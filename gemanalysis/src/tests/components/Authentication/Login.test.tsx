import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import Login from "../../../components/Authentication/Login";
import { useLogin } from "../../../service/reactQueryFiles/useLogin";
import { MemoryRouter } from "react-router-dom";

// Mock the react-query hook
jest.mock("../../../service/reactQueryFiles/useLogin", () => ({
  useLogin: jest.fn(),
}));

// Mock the navigate function
const mockNavigate = jest.fn();
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => mockNavigate,
}));

describe("Login Component", () => {
  const mockLoginFn = jest.fn();

  beforeEach(() => {
    // Reset mocks before each test
    (useLogin as jest.Mock).mockReturnValue({
      logInFn: mockLoginFn,
      isPending: false,
    });
    mockLoginFn.mockClear();
    mockNavigate.mockClear();
  });

  it("renders the login form correctly", () => {
    render(<Login />, { wrapper: MemoryRouter });
    expect(screen.getByText("Login")).toBeInTheDocument();
    expect(screen.getByLabelText("Enter Your Email")).toBeInTheDocument();
    expect(screen.getByLabelText("Enter Your Password")).toBeInTheDocument();
  });

  it("shows validation errors for empty fields", async () => {
    render(<Login />, { wrapper: MemoryRouter });

    const submitButton = screen.getByRole("button", { name: /submit/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      // The button is disabled initially
      expect(submitButton).toBeDisabled();
    });
  });

  it("enables submit button when form is valid", () => {
    render(<Login />, { wrapper: MemoryRouter });

    fireEvent.change(screen.getByLabelText("Enter Your Email"), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText("Enter Your Password"), {
      target: { value: "password123" },
    });

    const submitButton = screen.getByRole("button", { name: /submit/i });
    expect(submitButton).not.toBeDisabled();
  });

  it("calls the login function on form submission", async () => {
    render(<Login />, { wrapper: MemoryRouter });

    const emailInput = screen.getByLabelText("Enter Your Email");
    const passwordInput = screen.getByLabelText("Enter Your Password");
    const submitButton = screen.getByRole("button", { name: /submit/i });

    fireEvent.change(emailInput, { target: { value: "test@example.com" } });
    fireEvent.change(passwordInput, { target: { value: "password123" } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockLoginFn).toHaveBeenCalledWith(
        { email: "test@example.com", password: "password123" },
        { onSuccess: expect.any(Function) }
      );
    });
  });

  it("navigates to signup page on signup button click", () => {
    render(<Login />, { wrapper: MemoryRouter });
    const signUpButton = screen.getByRole("button", { name: /sign up/i });
    fireEvent.click(signUpButton);
    expect(mockNavigate).toHaveBeenCalledWith("/signup");
  });
});
