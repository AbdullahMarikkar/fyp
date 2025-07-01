import { wordFirstLetterUppercase } from "../../utils/utilFunctions";

describe("utilFunctions", () => {
  describe("wordFirstLetterUppercase", () => {
    it("should capitalize the first letter of a lowercase word", () => {
      expect(wordFirstLetterUppercase("test")).toBe("Test");
    });

    it("should not change a word that is already capitalized", () => {
      expect(wordFirstLetterUppercase("Test")).toBe("Test");
    });

    it("should handle an empty string", () => {
      expect(wordFirstLetterUppercase("")).toBe("");
    });

    it("should handle a single letter word", () => {
      expect(wordFirstLetterUppercase("a")).toBe("A");
    });
  });
});
