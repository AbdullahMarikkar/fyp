import { Box, CircularProgress } from "@mui/material";

function LoadingIndicator() {
  return (
    <Box
      sx={{
        position: "fixed", // Ensure it covers the screen
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        backdropFilter: "blur(5px)", // Blurs the background
        backgroundColor: "rgba(255, 255, 255, 0.3)", // Semi-transparent overlay
        zIndex: 9999, // Ensure it's on top
      }}
    >
      <CircularProgress size={80} />
    </Box>
  );
}

export default LoadingIndicator;
