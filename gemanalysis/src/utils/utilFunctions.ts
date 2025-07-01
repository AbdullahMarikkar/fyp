export function wordFirstLetterUppercase(word: string) {
  if (word.length > 0) {
    return word[0].toLocaleUpperCase() + word.slice(1);
  } else {
    return "";
  }
}
