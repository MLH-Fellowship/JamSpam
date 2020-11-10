/* Spam blob */
const spam = [
  "readme",
  "relevant issues",
  "relevant docstrings",
  "versionchanged directives",
  "changelog entry",
  "run automatically",
  "save time",
  "beginners create",
  "basic blogging",
  "main interface",
  "release noteshttpsgithub",
  "comevanwesbuildreleases changeloghttpsgithub",
  "fixes nnn",
  "additional information",
  "stepbystep reproduction",
  "create readmekorean",
  "event handling",
  "pr title",
  "contribution guide",
];

/* Check count of a substring in the string */
const counter = (main_str, sub_str) => {
  main_str += "";
  sub_str += "";

  if (sub_str.length <= 0) {
    return main_str.length + 1;
  }

  subStr = sub_str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return (main_str.match(new RegExp(subStr, "gi")) || []).length;
};

/* Count the total spam keywords in the PR */
const spam_count = (text_corpus) => {
  let count = 0;
  for (word of spam) {
    var countSpam = counter(text_corpus, word);
    count = count + countSpam;
  }
  return count;
};

module.exports = spam_count;
