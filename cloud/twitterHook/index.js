const crypto = require("crypto");
const Buffer = require("safe-buffer").Buffer;
const { PubSub } = require("@google-cloud/pubsub");
const projectId = "robust-habitat-247702";
const pubsub = new PubSub({ projectId });

/**
 *
 * @param {!Object} req Cloud Function request context.
 * @param {!Object} res Cloud Function response context.
 */
exports.twitterHook = (req, res) => {
  console.log("HEREDOR");
  console.log(req.body);
  if (req.method === "GET") {
    const crc_token = req.query.crc_token;
    if (crc_token) {
      const hmac = crypto
        .createHmac("sha256", process.env.APP_SECRET)
        .update(crc_token)
        .digest("base64");
      res.json({ response_token: "sha256=" + hmac });
      return;
    }
  } else if (req.method === "POST" && req.body) {
    let commands = [];
    if (req.body.for_user_id === process.env.BOT_USER) {
      if (req.body.tweet_create_events) {
        req.body.tweet_create_events.forEach((event) =>
          handleTweetCreateEvent(event, commands)
        );
      }
      if (req.body.message_data) {
        handleMessageData(req.body.sender_id, req.body.message_data, commands);
      }
      if (req.body.direct_message_events) {
        req.body.direct_message_events.forEach((event) => {
          if (event.message_create) {
            handleMessageData(
              event.message_create.sender_id,
              event.message_create.message_data,
              commands
            );
          }
        });
      }
    }
    publishCommandsToPubsub(commands, res);
    return;
  }
  // This is an error case, as "message" is required.
  res.status(400).send("Wrong method or empty");
};

function handleTweetCreateEvent(event, commands) {
  const senderId = event.user.id;
  const isMention = !!event.entities.user_mentions.find(
    (mention) => mention.id_str === process.env.BOT_USER
  );
  if (isMention) {
    tweetComponentsToCommand(senderId, event.text, event.entities, commands);
  }
}

function handleMessageData(senderId, messageData, commands) {
  tweetComponentsToCommand(
    senderId,
    messageData.text,
    messageData.entities,
    commands
  );
}

// Parses tweet components to a command and stores in the commands array if successful
function tweetComponentsToCommand(senderId, text, entities, commands) {
  // Important to at least reject the bot's user ID as the bot's direct messages with listing results will be sent to the webhook
  if (!senderId || !isUserAuthorized(senderId)) {
    return;
  }
  let command;
  if (isCommand(text, "list!")) {
    command = "list";
  } else if (entities.urls.length > 0) {
    command = "store";
  } else {
    return;
  }
  const message = {
    senderId: senderId,
    command: command,
    text: text,
    urls: entities.urls,
    tags: entities.hashtags
  };
  commands.push(message);
}

function publishCommandsToPubsub(commands, response) {
  if (commands.length > 0) {
    const publisher = pubsub.topic("commands").publisher();
    let remaining = commands.length;
    const callback = (err) => {
      if (err) {
        console.log("Failed to publish command: " + err);
      }
      remaining--;
      if (remaining === 0) {
        response.send(200);
      }
    };
    for (let i = 0; i < commands.length; i++) {
      publisher.publish(Buffer.from(JSON.stringify(commands[i])), callback);
    }
  } else {
    response.send(200);
  }
}

function isCommand(text, command) {
  const idx = text.toLowerCase().indexOf(command);
  return (
    idx >= 0 &&
    (idx === 0 || text.charAt(idx) === " ") &&
    (idx + command.length === text.length ||
      text.charAt(idx + command.length) === " ")
  );
}

function isUserAuthorized(userId) {
  return userId.toString() === process.env.MY_TWITTER_USER;
}
