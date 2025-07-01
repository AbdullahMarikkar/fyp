import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import SignUp from "../../../components/Authentication/SignUp";
import { useSignUp } from "../../../service/reactQueryFiles/useSignUp";
import { MemoryRouter } from "react-router-dom";

// Mocks
jest.mock("../../../service/reactQueryFiles/useSignUp", () => ({
  useSignUp: jest.fn(),
}));
const mockNavigate = jest.fn();
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => mockNavigate,
}));

describe("SignUp Component", () => {
  const mockSignUpFn = jest.fn();

  beforeEach(() => {
    (useSignUp as jest.Mock).mockReturnValue({
      signUpFn: mockSignUpFn,
      isPending: false,
    });
    mockSignUpFn.mockClear();
    mockNavigate.mockClear();
  });

  it("renders the signup form correctly", () => {
    render(<SignUp />, { wrapper: MemoryRouter });
    expect(screen.getByText("Sign Up")).toBeInTheDocument();
    expect(screen.getByLabelText("Enter Your Email")).toBeInTheDocument();
    expect(screen.getByLabelText("Enter Your Username")).toBeInTheDocument();
    expect(
      screen.getByLabelText("Enter Your Mobile Number")
    ).toBeInTheDocument();
    expect(screen.getByLabelText("Enter Your Password")).toBeInTheDocument();
  });

  it("calls the signup function with correct values on submit", async () => {
    render(<SignUp />, { wrapper: MemoryRouter });

    fireEvent.change(screen.getByLabelText("Enter Your Email"), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText("Enter Your Username"), {
      target: { value: "testuser" },
    });
    fireEvent.change(screen.getByLabelText("Enter Your Mobile Number"), {
      target: { value: "1234567890" },
    });
    fireEvent.change(screen.getByLabelText("Enter Your Password"), {
      target: { value: "password123" },
    });

    const submitButton = screen.getByRole("button", { name: /submit/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockSignUpFn).toHaveBeenCalledWith(
        {
          email: "test@example.com",
          username: "testuser",
          mobile: "1234567890",
          password: "password123",
        },
        { onSuccess: expect.any(Function) }
      );
    });
  });

  it("navigates to login page on login button click", () => {
    render(<SignUp />, { wrapper: MemoryRouter });
    const logInButton = screen.getByRole("button", { name: /log in/i });
    fireEvent.click(logInButton);
    expect(mockNavigate).toHaveBeenCalledWith("/login");
  });
});
