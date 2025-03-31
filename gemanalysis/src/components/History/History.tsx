import { Box, Button, Typography } from "@mui/material";
import Grid from "@mui/material/Grid2";
import {
  gridTableHeaderStyle,
  gridTableHeaderTextStyle,
  gridTableItemStyle,
  gridTableItemTextStyle,
} from "../../utils/constants";
import { useGetHistory } from "../../service/reactQueryFiles/useGetHistory";
import { useNavigate } from "react-router-dom";
import { wordFirstLetterUppercase } from "../../utils/utilFunctions";
import { removeAccessTokenFromCookie } from "../../utils/cookieService";
import LoadingIndicator from "../../utils/LoadingIndication";

export interface HistoryType {
  id: number;
  name: string;
  gem_type: string;
  result: string;
  satisfactory: string;
  user_id: number;
  image: string | null;
}

function History() {
  const navigate = useNavigate();
  const { history, isLoading } = useGetHistory();
  if (isLoading) {
    return <LoadingIndicator />;
  }

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
          justifyContent: "flex-end",
          alignItems: "center",
          padding: "10px",
        }}
      >
        <Button
          onClick={() => navigate("/")}
          variant="contained"
          sx={{ borderRadius: "30px" }}
        >
          Home
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
          sx={{ color: "purple", fontSize: "35px", paddingBottom: "20px" }}
          textAlign="center"
        >
          History
        </Typography>
        <Box
          sx={{
            width: "100%",
            borderRadius: "5px",
            display: "flex",
            flexDirection: "column",
            gap: "10px",
          }}
        >
          <Grid
            container
            key={"table-head"}
            columns={{ xs: 6.5, sm: 13.5 }}
            sx={{ width: "100%" }}
          >
            <Grid size={"auto"} sx={gridTableHeaderStyle} minWidth={"160px"}>
              <Typography sx={gridTableHeaderTextStyle}>Gem Image</Typography>
            </Grid>
            <Grid size={"grow"} sx={gridTableHeaderStyle}>
              <Typography sx={gridTableHeaderTextStyle}>Gem Type</Typography>
            </Grid>
            <Grid size={"grow"} sx={gridTableHeaderStyle}>
              <Typography sx={gridTableHeaderTextStyle}>Result</Typography>
            </Grid>
            <Grid size={"grow"} sx={gridTableHeaderStyle}>
              <Typography sx={gridTableHeaderTextStyle}>Satisfied</Typography>
            </Grid>
          </Grid>
          {history?.data.map((gems: HistoryType, i: number) => {
            return (
              <Grid
                container
                columns={{ xs: 6.5, sm: 13.5 }}
                sx={{ width: "100%" }}
                key={i}
              >
                <Grid size={"auto"} sx={gridTableItemStyle} maxWidth={"160px"}>
                  {/* <Typography sx={gridTableItemTextStyle}>{i + 1}</Typography> */}
                  <img
                    src={
                      gems.image
                        ? `data:image/jpeg;base64, ${gems.image as string}`
                        : undefined
                    }
                    style={{
                      height: "150px",
                      width: "150px",
                      borderRadius: "20px",
                    }}
                  />
                </Grid>
                <Grid size={"grow"} sx={gridTableItemStyle}>
                  <Typography sx={gridTableItemTextStyle}>
                    {wordFirstLetterUppercase(gems.gem_type)}
                  </Typography>
                </Grid>
                <Grid size={"grow"} sx={gridTableItemStyle}>
                  <Typography sx={gridTableItemTextStyle}>
                    {wordFirstLetterUppercase(gems.result)}
                  </Typography>
                </Grid>
                <Grid size={"grow"} sx={gridTableItemStyle}>
                  <Typography sx={gridTableItemTextStyle}>
                    {wordFirstLetterUppercase(gems.satisfactory)}
                  </Typography>
                </Grid>
              </Grid>
            );
          })}
        </Box>
      </Box>
    </Box>
  );
}

export default History;
