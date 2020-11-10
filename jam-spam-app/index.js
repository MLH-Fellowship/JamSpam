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

  async function getStarted() {
    const model = await loadLayersModel(`file://${process.cwd()}/model/model.json`);
    var res = model.predict(tensor([[1, 0, 2, 4, 0], [2567, 490, 5, 260357, 0], [9, 0, 6, 627, 0]]))
    app.log.debug(res.dataSync())
  }

  async function close (context, params) {
    const closeParams = Object.assign({}, params, {state: 'closed'})
  
    return context.github.issues.edit(closeParams)
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
      // skip spam check - verified userconst files_changed = pull_request.changed_files;
      try{
      const files_changed =  parseInt(pull_request.changed_files);
      const commits =  parseInt(pull_request.commits);
      const title1 =  pull_request.title.toString();
      const body1 =  pull_request.body.toString();
      const changes =  parseInt(pull_request.additions) + parseInt(pull_request.deletions);
      const {spam_counted,docschange} = await fetchText(pull_request.diff_url).then(diff => {
        const textblob = title1 + body1 + diff
        const spam_counted = spam_count(textblob)
        const docschange = docschanged(diff)
        return {spam_counted, docschange}
      });  
      app.log.info(files_changed,commits,changes,docschange,spam_counted);
      console.log(files_changed,commits,changes,spam_counted,docschange);
      const prComment = context.issue({ body: 'This pull is not spam. The contributor is legit.' })
      return context.github.issues.createComment(prComment)
      }
      catch(e){
        app.log.info(e);
      }
    }
    else if (["FIRST_TIMER", "MANNEQUIN", "FIRST_TIME_CONTRIBUTOR", "NONE", ""].includes(pull_request.author_association)){
      // possibly spam - check for spam in classifier
      const files_changed = pull_request.changed_files;
      const commits = pull_request.commits;
      const title = pull_request.title;
      const body = pull_request.body;
      const changes = pull_request.additions + pull_request.deletions
      const diff = fetchText(pull_request.diff_url)
      const textblob = title + body + diff 
      const spam_counted = spam_count(textblob)
      const docschange = docschanged(diff)
      console.log(files_changed)
      console.log(changes)
      console.log(docschange)
      console.log(commits)
      console.log(spam_counted)
      const prComment = context.issue({ body: 'This pull request might be spam. Further review needed.' })
      return context.github.issues.createComment(prComment)
    }
  })

  // For more information on building apps:
  // https://probot.github.io/docs/

  // To get your app running against GitHub, see:
  // https://probot.github.io/docs/development/
}
