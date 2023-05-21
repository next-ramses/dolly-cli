from textual import events
from textual.app import (
    App,
    ComposeResult,
)
from textual.widgets import (
    Header,
    Input,
    TextLog,
    LoadingIndicator,
    ContentSwitcher,
)
from textual.css.query import NoMatches
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)
import torch
from MODELFOLDER.instruct_pipeline import InstructionTextGenerationPipeline

class ChatApp(App):
    CSS_PATH = "dolly.css"
    TITLE = "Chat with Dolly 2.0"

    def compose(self) -> ComposeResult:
        with ContentSwitcher(initial="prompt", id="switcher"):
            yield Input("", placeholder="Enter a prompt", id="prompt")
            yield LoadingIndicator(id="thinking")
        yield TextLog(wrap=True, id="history")
        yield Header()

    def on_key(self, event: events.Key) -> None:
        if event.key == "q":
            self.app.exit()
        if event.key == "enter":
            try:
                input_element = self.query_one(Input)
            except NoMatches:
                return
            content_switcher = self.query_one(ContentSwitcher)
            prompt = input_element.value
            if not prompt:
                return
            text_log_element = self.query_one(TextLog)
            text_log_element.write(f"> {prompt}")
            input_element.value = ""
            content_switcher.current = "thinking" # not working
            result = generate_text(prompt)[0]["generated_text"]
            text_log_element.write(f"- {result}\n")
            content_switcher.current = "prompt"
        

app = ChatApp()

print("Loading model, please wait...")
tokenizer = AutoTokenizer.from_pretrained("MODELFOLDER", padding_side="left")
model = AutoModelForCausalLM.from_pretrained("MODELFOLDER", device_map="auto", torch_dtype=torch.bfloat16)
generate_text = InstructionTextGenerationPipeline(model=model, tokenizer=tokenizer)

app.run()

