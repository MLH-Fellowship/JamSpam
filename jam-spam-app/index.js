/**
 * This is the main entrypoint to your Probot app
 * @param {import('probot').Application} app
 */
module.exports = app => {
  // Your code here
  app.log.info('Yay, the app was loaded!')

  app.on('issues.opened', async context => {
    const issueComment = context.issue({ body: 'Thanks for opening this issue!' })
    return context.github.issues.createComment(issueComment)
  })

  app.on('pull_request.opened', async context => {
    app.log.info(context);
    if (context.payload.pull_request.author_association == "FIRST_TIMER" || context.payload.pull_request.author_association == "MANNEQUIN" || context.payload.pull_request.author_association == "FIRST_TIME_CONTRIBUTOR" || context.payload.pull_request.author_association == "NONE"){
      const prComment = context.issue({ body: 'This pull request might be spam. Further review needed.' })
      return context.github.issues.createComment(prComment)
    }
    else{
      const prComment = context.issue({ body: 'This pull is not spam. The contributor is legit.' })
      return context.github.issues.createComment(prComment)
    }
  })

  // For more information on building apps:
  // https://probot.github.io/docs/

  // To get your app running against GitHub, see:
  // https://probot.github.io/docs/development/
}
