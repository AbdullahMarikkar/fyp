import torch.nn as nn
import torchvision.models as models


class SingleHeadModel(nn.Module):
    """
    A flexible transfer learning model that automatically adapts its
    classification head to different PyTorch model architectures.
    """

    def __init__(self):
        super(SingleHeadModel, self).__init__()

        # --- 1. Load the pre-trained model ---
        # You can easily swap the model you want to test here.
        # NOTE: `pretrained=True` is the older method. The modern approach is to use the `weights`
        # parameter, e.g., models.squeezenet1_0(weights=models.SqueezeNet1_0_Weights.DEFAULT)
        # I am using `pretrained=True` to match your original code.

        self.base_model = models.resnet152can(pretrained=True)
        # self.base_model = models.resnet18(pretrained=True)
        # self.base_model = models.efficientnet_v2_s(pretrained=True)

        # --- 2. Freeze the weights of the pre-trained layers ---
        # This ensures we only train our new custom classifier layer.
        for param in self.base_model.parameters():
            param.requires_grad = False

        # --- 3. Intelligently replace the final classifier layer ---
        # This section specifically handles the different structures of popular model families.

        # Get the name of the model's class to identify its family
        model_name = self.base_model.__class__.__name__

        if model_name in ["SqueezeNet"]:
            # SqueezeNet uses a Conv2d layer at index 1 of its classifier for classification.
            # We get its input channels and replace it with a new Conv2d layer for our 3 classes.
            num_input_channels = self.base_model.classifier[1].in_channels
            self.base_model.classifier[1] = nn.Conv2d(
                num_input_channels, 3, kernel_size=(1, 1)
            )
            self.base_model.num_classes = 3  # Update the model's class count attribute

        elif model_name in ["EfficientNet"]:
            # EfficientNet models have a Linear layer at the end of their classifier sequence.
            num_input_features = self.base_model.classifier[-1].in_features
            # We replace the entire classifier with a new sequence containing our Linear layer.
            self.base_model.classifier = nn.Sequential(
                nn.Dropout(p=0.3, inplace=True),
                nn.Linear(num_input_features, 3),  # 3 output classes
            )

        elif model_name in [
            "VGG",
            "ShuffleNetV2",
            "MobileNetV3",
            "Inception3",
            "ResNet",
            "EfficientNetV2",
            "ConvNeXt",
            "VisionTransformer",
        ]:
            # ResNet and similar models use a single Linear layer named 'fc'.
            if hasattr(self.base_model, "fc"):
                num_input_features = self.base_model.fc.in_features
                self.base_model.fc = nn.Linear(num_input_features, 3)
            # VGG/AlexNet use a classifier sequence with a final Linear layer.
            elif hasattr(self.base_model, "classifier") and isinstance(
                self.base_model.classifier, nn.Sequential
            ):
                num_input_features = self.base_model.classifier[-1].in_features
                self.base_model.classifier[-1] = nn.Linear(num_input_features, 3)
            else:
                raise NotImplementedError(
                    f"Classifier replacement for {model_name} is not implemented."
                )

        else:
            # This error will trigger if you try a model family not yet handled.
            raise NotImplementedError(
                f"Model family '{model_name}' is not supported yet. Please add a specific handler for it."
            )

    def forward(self, x):
        """Defines the forward pass; it simply calls the entire modified base model."""
        outputs = self.base_model(x)

        # During training, InceptionV3 returns a special InceptionOutputs object.
        # We must extract the primary output (logits) for the loss calculation.
        if self.training and isinstance(outputs, models.inception.InceptionOutputs):
            return outputs.logits

        # During evaluation, or for other models, it returns a single tensor.
        return outputs
