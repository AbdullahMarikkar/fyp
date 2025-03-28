import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import DashBoardScreen from "./screens/DashboardScreen";

// TODO : MAIN COLORS
// #8174A0
// #A888B5
// #EFB6C8
// #FFD2A0

function App() {
  return (
    <>
      <ReactQueryDevtools />
      <DashBoardScreen />
    </>
  );
}

export default App;
