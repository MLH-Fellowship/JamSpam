const { loadLayersModel, tensor } = require('@tensorflow/tfjs-node')
tf = require('@tensorflow/tfjs-node')
const spam_count = require('./checkspamcount')
const fetchText = require('./fetchtext')
const docschanged = require ('./docschanged')
/**
 * This is the main entrypoint to your Probot app
 * @param {import('probot').Application} app
 */


module.exports = app => {
  // Your code here
  app.log.info('Yay, the app was loaded!')

  var model = null;
  var SPAM_THRESHOLD = 0.90;

  async function getStarted() {
    model = await loadLayersModel(`file://${process.cwd()}/model/model.json`);
  }

  async function close (context, params) {
    const closeParams = Object.assign({}, params, {state: 'closed'})
    return context.github.issues.update(closeParams)
  }

  async function predict (inputTensor) {
    var res = await model.predict(inputTensor)
    var spam_prob = res.dataSync()[0]
    return spam_prob > SPAM_THRESHOLD
  }

  getStarted();

  app.on('issues.opened', async context => {
    const issueComment = context.issue({ body: 'Thanks for opening this issue!' })
    return context.github.issues.createComment(issueComment)
  })

  app.on('pull_request.opened', async context => {
    // app.log.info(context);
    var pull_request = context.payload.pull_request;
    try {
      const files_changed =  parseInt(pull_request.changed_files);
      const commits =  parseInt(pull_request.commits);
      const title1 =  pull_request.title.toString();
      const body1 =  pull_request.body.toString();
      const changes =  parseInt(pull_request.additions) + parseInt(pull_request.deletions);
      const {spam_counted, docschange} = await fetchText(pull_request.diff_url).then(diff => {
        const textblob = title1 + body1 + diff
        const spam_counted = spam_count(textblob)
        const docschange = docschanged(diff)
        return {spam_counted, docschange}
      });  
      var inputTensor = tensor([[files_changed, docschange, commits, changes, spam_counted]]);
      // app.log.info(inputTensor);
    }
    catch(e){
      app.log.error(`Error: ${e}`);
    }
    var isSpam = await predict(inputTensor);
    if (["COLLABORATOR", "CONTRIBUTOR", "MEMBER", "OWNER"].includes(pull_request.author_association) || !isSpam){
      // skip spam check - verified userconst files_changed = pull_request.changed_files;
      const prComment = context.issue({ 
        body: `Thanks for your Pull Request @${pull_request.user.login} 🙌 This seems like a legit 💯 contribution` 
      });
      return context.github.issues.createComment(prComment);
    }
    else if (["FIRST_TIMER", "MANNEQUIN", "FIRST_TIME_CONTRIBUTOR", "NONE", ""].includes(pull_request.author_association) && isSpam){
      // possibly spam - check for spam in classifier
      const prComment = context.issue({ 
        body: `Hmmm, something is fishy 🐠 here! We think this Pull Request does not meet the standards. 
        Kindly refer to the Contributing Guidelines of the project. We look forward to your future contributions!` 
      });
      await context.github.issues.createComment(prComment)
      return close(context, context.issue())
    }
  })

  // For more information on building apps:
  // https://probot.github.io/docs/

  // To get your app running against GitHub, see:
  // https://probot.github.io/docs/development/
}
