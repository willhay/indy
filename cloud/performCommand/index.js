const request = require("request");
const { Datastore } = require("@google-cloud/datastore");
const datastore = new Datastore();
const Buffer = require("safe-buffer").Buffer;
const NEW_DIRECT_MESSAGE_ENDPOINT =
  "https://api.twitter.com/1.1/direct_messages/events/new.json";

/**
 * Triggered from a message on a Cloud Pub/Sub topic.
 *
 * @param {!Object} event Event payload and metadata.
 * @param {!Function} callback Callback function to signal completion.
 */
exports.performCommand = (event, ctx, callback) => {
  const pubsubMessage = event.data;
  const message = JSON.parse(Buffer.from(pubsubMessage, "base64").toString());
  handleMessage(
    message.command,
    message.senderId,
    message.text,
    message.urls,
    message.tags,
    callback
  );
};

function handleMessage(
  command,
  senderId,
  text,
  urls,
  tags,
  completionCallback
) {
  if (command === "list") {
    listAndSend(senderId, 0, tags, completionCallback);
  } else if (command === "store") {
    storeLink(senderId, urls[0], tags, completionCallback);
  } else {
    console.log("Unknown command: " + command);
    completionCallback();
  }
}

function listAndSend(senderId, token, hashtags, completionCallback) {
  let q = datastore
    .createQuery(["Url"])
    .hasAncestor(datastore.key(["User", datastoreIdFromTwitterUser(senderId)]))
    .limit(3);
  let tags = hashtags.map((tag) => tag.text);
  for (let i = 0; i < tags.length; i++) {
    q = q.filter("tags", "=", tags[i]);
  }
  datastore.runQuery(q, (err, entities, nextQuery) => {
    if (err) {
      console.log("Error when querying entities " + err);
      completionCallback();
      return;
    }
    // const hasMore = nextQuery.moreResults !== Datastore.NO_MORE_RESULTS ? nextQuery.endCursor : false;
    // const links = entities.map((entity) => entity[datastore.KEY].name);
    // sendLinks(senderId, links, token, hasMore, completionCallback);
  });
}

// function sendLinks(senderId, links, offset, hasMore, completionCallback) {
//   let text = links.length == 0 ? "No links found" : "";
//   for (let i = 0; i < links.length; i++) {
//     if (i != 0) {
//       text += " ";
//     }
//     text += (i + offset + 1) + ". " + links[i];
//   }
//   const message = {
//     "event": {
//       "type": "message_create",
//       "message_create": {
//         "target": {
//           "recipient_id": senderId
//         },
//         "message_data": {
//           "text": text,
//         }
//       }
//     }
//   };
//   request({
//     url: NEW_DIRECT_MESSAGE_ENDPOINT,
//     oauth: {
//       consumer_key: process.env.APP_KEY,
//       consumer_secret: process.env.APP_SECRET,
//       token: process.env.TOKEN,
//       token_secret: process.env.TOKEN_SECRET
//     },
//   	method: "POST",
//   	json: message})
//     .on("response", function(resp) {
//     	if (resp.statusCode > 299) {
//           console.log("Failed to send list message, status code " + resp.statusCode);
//           console.log(resp);
//         }
//         completionCallback();
//   	})
//   	.on("error", function(err) {
//     	console.log("Failed to send list message: " + err);
//     	completionCallback();
//   	});
// };

function storeLink(senderId, url, hashtags, completionCallback) {
  const key = datastore.key([
    "User",
    datastoreIdFromTwitterUser(senderId),
    "Url",
    url.expanded_url
  ]);
  const data = {
    tags: hashtags.map((tag) => tag.text)
  };
  const entity = {
    key: key,
    data: data
  };
  datastore
    .save(entity)
    .then(() => {
      completionCallback();
    })
    .catch((err) => {
      console.error(err);
      completionCallback();
    });
}

// Storing the source of the user ID in the data model to support adding other modes of entry
// Better done with a separate property in the datastore, as the prefix makes sorted searches less efficient
function datastoreIdFromTwitterUser(id) {
  return "tw:" + id;
}
