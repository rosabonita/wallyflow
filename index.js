const Alexa = require('alexa-sdk');
const AWS = require('aws-sdk');
const APP_ID = 'amzn1.ask.skill.1a61b436-2b39-448c-a2bb-1ad391fe666b';
const handlers = {

  "AboutMindfulnessIntent": function () {
    var speechOutput = "Mindfulness is the quality or state of being concious or aware of something. ";
    this.emit(':tell', speechOutput);
  },

  "AboutWallyFlowIntent": function () {
    var speechOutput = "Wally Flow helps you be more mindful by gently raising your awareness of periods of extended inactivity.";
    this.emit(':tell',speechOutput);
  },

  "AboutWalabot": function() {
    var speechOutput = "Walabot is a programmable 3D imaging sensor. It has flexible sensor system with between 3 and 18 antennas. Walabot can see through solid objects, track movements, and detect surroundings and speed. To purchase a Walabot, go to Walabot.com. ";
    this.emit(':tell', speechOutput);
  },

  "AMAZON.HelpIntent": function () {
    var speechOutput = "Here are some things you can say. Tell me about Walabot. Tell me about Wally Flow. Tell me about Mindfulness. You can also say stop if you're done. So how can I help?";
    this.emit(':ask',speechOutput,speechOutput);
  },

  "AMAZON.StopIntent": function () {
    var speechOutput = "Goodbye";
    this.emit(':tell', speechOutput);
  },

  "AMAZON.CancelIntent": function () {
    var speechOutput = "Goodbye";
    this.emit(':tell', speechOutput);
  },

  "LaunchRequest": function () {
    var speechText = "Welcome to Wally Flow. ";
    var repromptText = "For instructions on what you can say, please say help me.";
    this.emit(':tell',speechText,repromptText);
  }
};

exports.handler = function(event, context, callback) {
    const alexa = Alexa.handler(event, context, callback);
    alexa.appId = APP_ID
    alexa.registerHandlers(handlers);
    alexa.execute();
};
