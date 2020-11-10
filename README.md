# JamSpam

> A Machine Learning powered GitHub App built with [Probot](https://github.com/probot/probot) to jam the spam PRs on your repo and keep maintainers stress-free (even in Hacktober 🎃)

## Summary

### Building Dataset

- We listed links of PRs labelled as ⚠ `SPAM` or `INVALID` ⚠ on some popular repositories especially those that faced a pool of spam pull-requests during the recently concluded Hacktoberfest 🎃 in a [`.csv` file](jam-spam-ml/data/spam.csv).
- Similarly, we also listed links of ✅ `MERGED` PRs on the repositories in a separate [`.csv` file](jam-spam-ml/data/ham.csv) for Ham (not Spam) features.
- We used [Octokit](https://octokit.github.io/), an API framework by GitHub to extract Pull Request Information from the PR links and save desired features locally to build our model.

### Feature Extraction

We chose the standard PR attributes and some derived features to train our model

- **Standard**
    - *Number of Commits*
    - *Number of Files Changed*
    - *Number of Changes* `(Additions + Deletions)`
- **Derived**
    - *Number of Files Changed of Documentation Type*
        ```py
        # File Extensions considered to be of Doc-Type 
        ['md', 'txt', 'rst', '']
        ```
    - *Occurences of spam hit-words in text corpus of PR*
        
        Text Corpus of a Pull Request includes the PR Title, Body, Commit Messages and Diffs.

        All text is pre-processed with regex to exclude any symbols.

### Model Design 

We are using Keras to build our baseline model. It is essentially a (5-16-16-1) Sequential Neural Network with first three layers being 'RELU' activated and the final output layer activated as a sigmoid function.

The model is run over 500 epochs with a unit batch size.

### Transfer Model to Bot

The model is exported from Python using `tensorflowjs` that creates a `model.json` and a `.bin` file to store the model structure, variables and associated weights.

The model is imported seamlessly into Node.js using `@tensorflow/tfjs-node` for predictions to be made for incoming PRs

## Getting Started

- For setup instructions to train and export the model, visit [jam-spam-ml/README.md](jam-spam-ml/README.md)
- For setup instructions to build the bot and getting the GitHub App running, head to [jam-spam-app/README.md]([jam-spam-app/README.md])

## Contributing

If you have suggestions for how JamSpam could be improved, or want to report a bug, open an issue! We'd love all and any contributions.

For more, check out the [Contributing Guide](CONTRIBUTING.md).

## License

[MIT](LICENSE) © 2020 MLH Fellowship

Made with :heart: by [Ajwad Shaikh](https://github.com/ajwad-shaikh) & [Vrushti Mody](https://github.com/vrushti-mody) during Sprint 3 of the MLH Fellowship Explorer Batch, Fall 2020.
