// src/__tests__/components/History/History.test.tsx

// Mock the universal-cookie library
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

import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import History from "../../../components/History/History";
import { useGetHistory } from "../../../service/reactQueryFiles/useGetHistory";
import { MemoryRouter } from "react-router-dom";

// Mocks for other dependencies
jest.mock("../../../service/reactQueryFiles/useGetHistory");
const mockNavigate = jest.fn();
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => mockNavigate,
}));

describe("History Component", () => {
  // ... rest of your tests remain the same
  it("shows loading indicator when data is loading", () => {
    (useGetHistory as jest.Mock).mockReturnValue({
      isLoading: true,
      history: null,
    });
    render(<History />, { wrapper: MemoryRouter });
    expect(screen.getByRole("progressbar")).toBeInTheDocument();
  });

  // src/__tests__/components/History/History.test.tsx

  it("renders history data correctly", () => {
    const mockHistoryData = {
      data: [
        {
          id: 1,
          name: "gem1.jpg",
          gem_type: "sapphire",
          result: "heated",
          satisfactory: "satisfied",
          image: "base64-encoded-string-1",
        },
        {
          id: 2,
          name: "gem2.jpg",
          gem_type: "ruby",
          result: "natural",
          satisfactory: "neutral",
          image: "base64-encoded-string-2",
        },
      ],
    };
    (useGetHistory as jest.Mock).mockReturnValue({
      isLoading: false,
      history: mockHistoryData,
    });

    render(<History />, { wrapper: MemoryRouter });

    expect(screen.getByText("History")).toBeInTheDocument();

    // Use getAllByText for any text that might appear more than once.
    // Then, check that at least one instance was found.
    expect(screen.getAllByText("Sapphire")[0]).toBeInTheDocument();
    expect(screen.getAllByText("Heated")[0]).toBeInTheDocument();
    expect(screen.getAllByText("Satisfied")[0]).toBeInTheDocument(); // This now works!
    expect(screen.getAllByText("Ruby")[0]).toBeInTheDocument();
    expect(screen.getAllByText("Natural")[0]).toBeInTheDocument();
    expect(screen.getAllByText("Neutral")[0]).toBeInTheDocument();
  });
});
