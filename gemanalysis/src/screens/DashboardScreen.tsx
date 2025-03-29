import { Typography, Box, Button } from "@mui/material";
import ImageDropZone from "../components/ImageDropZone/ImageDropZone";
import { useNavigate } from "react-router-dom";
import { removeAccessTokenFromCookie } from "../utils/cookieService";

function DashBoardScreen() {
  const navigate = useNavigate();
  return (
    <Box
      sx={{
        background:
          "linear-gradient(38deg, rgba(2,0,36,0.9747548677674195) 0%, #dadcb2 29%, #8adaee 93%)",
        minWidth: "100vh",
        minHeight: "100vh",
        // opacity: "70%",
      }}
    >
      <Box
        sx={{
          display: "flex",
          justifyContent: "flex-end",
          alignItems: "center",
          padding: "10px",
        }}
      >
        <Button
          onClick={() => navigate("/history")}
          variant="contained"
          sx={{ borderRadius: "30px" }}
        >
          History
        </Button>
        <Button
          onClick={() => {
            removeAccessTokenFromCookie();
            navigate("/login");
          }}
        >
          Logout
        </Button>
      </Box>
      <Typography
        textAlign="center"
        fontWeight="bold"
        fontSize="30px"
        color="#6d608c"
      >
        Inclusion Classifier
      </Typography>
      <Typography
        textAlign="center"
        fontWeight="bold"
        color="#8174A0"
        fontSize="25px"
      >
        Drop Inclusion Image for Result
      </Typography>

      <ImageDropZone />
    </Box>
  );
}

export default DashBoardScreen;
