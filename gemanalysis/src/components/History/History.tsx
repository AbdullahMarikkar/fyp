import { Box, CircularProgress, Typography } from "@mui/material";
import { useGetHistory } from "../../service/reactQueryFiles/useGetHistory";

function History() {
  const { history, isLoading } = useGetHistory();
  if (isLoading) <CircularProgress />;
  console.log("History", history);
  return (
    <Box
      sx={{
        background:
          "linear-gradient(9deg, rgba(2,0,36,0.3585083691679797) 0%, rgba(153,228,141,0.980357108663778) 40%, rgba(0,223,255,1) 92%)",
        minWidth: "100vh",
        minHeight: "100vh",
      }}
    >
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "flex-start",
          alignItems: "center",
          minHeight: "100vh",
          minWidth: "100vh",
        }}
      >
        <Typography
          sx={{ color: "purple", fontSize: "25px" }}
          textAlign="center"
        >
          History
        </Typography>
        <Box sx={{ width: "100%", display: "flex", flexDirection: "column" }}>
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-evenly",
              alignItems: "center",
            }}
          >
            <Typography
              textAlign="center"
              sx={{ border: 1, borderRadius: "10px", width: "20%" }}
            >
              Title
            </Typography>
            <Typography
              textAlign="center"
              sx={{ border: 1, borderRadius: "10px", width: "20%" }}
            >
              Title
            </Typography>
            <Typography
              textAlign="center"
              sx={{ border: 1, borderRadius: "10px", width: "20%" }}
            >
              Title
            </Typography>
            <Typography
              textAlign="center"
              sx={{ border: 1, borderRadius: "10px", width: "20%" }}
            >
              Title
            </Typography>
          </Box>
          {[1, 2, 3, 4, 5].map(() => (
            <Box
              sx={{
                display: "flex",
                justifyContent: "space-evenly",
                alignItems: "center",
              }}
            >
              <Typography
                textAlign="center"
                sx={{ border: 1, borderRadius: "10px", width: "20%" }}
              >
                Content
              </Typography>
              <Typography
                textAlign="center"
                sx={{ border: 1, borderRadius: "10px", width: "20%" }}
              >
                Content
              </Typography>
              <Typography
                textAlign="center"
                sx={{ border: 1, borderRadius: "10px", width: "20%" }}
              >
                Content
              </Typography>
              <Typography
                textAlign="center"
                sx={{ border: 1, borderRadius: "10px", width: "20%" }}
              >
                Content
              </Typography>
            </Box>
          ))}
        </Box>
      </Box>
    </Box>
  );
}

export default History;
