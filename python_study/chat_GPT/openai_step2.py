import os
import openai
openai.organization = "org-BRTbkUgOGRGwgGz1gjHfpv1X"
openai.api_key = "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"

import { Configuration, OpenAIApi } from "openai";
openai.api_key = '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'
const configuration = new Configuration({
    organization: "org-BRTbkUgOGRGwgGz1gjHfpv1X",
    apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);
const response = await openai.listEngines();