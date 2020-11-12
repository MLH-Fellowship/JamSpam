/* Spam blob */
const spam = [
  "versionchanged directives",
  "save time",
  "existing algorithm",
  "existing functionality",
  "naming conventions",
  "understand areas",
  "changelog entry",
  "run automatically",
  "style guidelines",
  "md file",
  "filename follow",
  "auto close",
  "update readme",
  "contributing document",
  "update contributing",
  "relevant docstrings",
  "relevant motivation",
  "relevant issues",
  "pr fixes",
  "breaking change",
  "change requires",
  "delete options",
  "added tests",
  "update change",
  "quickly create",
  "provide instructions",
  "md describe",
  "issue exists",
  "change add",
  "feature works",
  "documentation update",
  "relevant details",
  "test configuration",
];

/* Check count of a substring in the string */
const counter = (main_str, sub_str) => {
  main_str += "";
  sub_str += "";
  return (main_str.match(new RegExp(sub_str, "gi")) || []).length;
};

/* Count the total spam keywords in the PR */
const spam_count = (text_corpus) => {
  let count = 0;
  text_corpus = text_corpus.replace(/[^a-zA-Z0-9 \n\.]/g, ' ');
  for (word of spam) {
    var countSpam = counter(text_corpus, word);
    count = count + countSpam;
  }
  return count;
};

module.exports = spam_count;
