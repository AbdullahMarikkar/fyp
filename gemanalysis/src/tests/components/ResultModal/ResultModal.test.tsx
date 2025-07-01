import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import ResultModal from "../../../components/ResultModal/ResultModal";
import { useSendSatisfaction } from "../../../service/reactQueryFiles/useSendSatisfaction";

jest.mock("../../../service/reactQueryFiles/useSendSatisfaction");
jest.mock("universal-cookie", () => {
  const mockGet = jest.fn((name) => {
    if (name === "accessToken") {
      return "mock-access-token";
    }
    return null;
  });
  const mockConstructor = jest.fn(() => ({
    get: mockGet,
  }));
  return {
    __esModule: true,
    default: mockConstructor,
  };
});

describe("ResultModal Component", () => {
  const mockSendSatisfactionFn = jest.fn();
  const mockClose = jest.fn();

  const mockMessage = {
    result: "natural",
    filename: "test.jpg",
    gemType: "sapphire",
  };
  const mockImage = [{ src: "some-image-src" }];

  beforeEach(() => {
    (useSendSatisfaction as jest.Mock).mockReturnValue({
      sendSatisfactionFn: mockSendSatisfactionFn,
    });
    mockSendSatisfactionFn.mockClear();
    mockClose.mockClear();
  });

  it("renders modal with correct data when open", () => {
    render(
      <ResultModal
        open={true}
        close={mockClose}
        sentImage={mockImage}
        message={mockMessage}
      />
    );

    expect(screen.getByText("Result")).toBeInTheDocument();
    expect(screen.getByText("NATURAL")).toBeInTheDocument();
    expect(screen.getByLabelText("Neutral")).toBeChecked();
  });

  it("does not render when open is false", () => {
    const { container } = render(
      <ResultModal
        open={false}
        close={mockClose}
        sentImage={mockImage}
        message={mockMessage}
      />
    );
    // The modal is rendered in a portal, so we check if the container is empty
    expect(container.firstChild).toBeNull();
  });

  it("updates satisfaction value on radio button click", () => {
    render(
      <ResultModal
        open={true}
        close={mockClose}
        sentImage={mockImage}
        message={mockMessage}
      />
    );

    const satisfiedRadio = screen.getByLabelText("Satisfied");
    fireEvent.click(satisfiedRadio);
    expect(satisfiedRadio).toBeChecked();
  });

  it("calls sendSatisfactionFn with the correct payload on submit", async () => {
    render(
      <ResultModal
        open={true}
        close={mockClose}
        sentImage={mockImage}
        message={mockMessage}
      />
    );

    const unsatisfiedRadio = screen.getByLabelText("Unsatisfied");
    fireEvent.click(unsatisfiedRadio);

    const submitButton = screen.getByRole("button", { name: /submit/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockSendSatisfactionFn).toHaveBeenCalledWith(
        {
          filename: "test.jpg",
          gem_type: "sapphire",
          result: "natural",
          satisfactory: "unsatisfied",
        },
        { onSuccess: expect.any(Function) }
      );
    });
  });
});
