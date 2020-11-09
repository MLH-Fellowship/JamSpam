const { loadLayersModel, tensor } = require('@tensorflow/tfjs-node')

tf = require('@tensorflow/tfjs-node')
/**
 * This is the main entrypoint to your Probot app
 * @param {import('probot').Application} app
 */
module.exports = app => {
  // Your code here
  app.log.info('Yay, the app was loaded!')

  async function getStarted() {
    const model = await loadLayersModel(`file://${process.cwd()}/model/model.json`);
    var res = model.predict(tensor([[1, 0, 2, 4, 0], [2567, 490, 5, 260357, 0], [9, 0, 6, 627, 0]]))
    app.log.debug(res.dataSync())
  }

  getStarted();

  app.on('issues.opened', async context => {
    const issueComment = context.issue({ body: 'Thanks for opening this issue!' })
    return context.github.issues.createComment(issueComment)
  })

  app.on('pull_request.opened', async context => {
    app.log.info(context);
    var pull_request = context.payload.pull_request;
    if (["COLLABORATOR", "CONTRIBUTOR", "MEMBER", "OWNER"].includes(pull_request.author_association)){
      // skip spam check - verified user
      const prComment = context.issue({ body: 'This pull is not spam. The contributor is legit.' })
      return context.github.issues.createComment(prComment)
    }
    else if (["FIRST_TIMER", "MANNEQUIN", "FIRST_TIME_CONTRIBUTOR", "NONE", ""].includes(pull_request.author_association)){
      // possibly spam - check for spam in classifier
      const prComment = context.issue({ body: 'This pull request might be spam. Further review needed.' })
      return context.github.issues.createComment(prComment)
    }
  })

  // For more information on building apps:
  // https://probot.github.io/docs/

  // To get your app running against GitHub, see:
  // https://probot.github.io/docs/development/
}
