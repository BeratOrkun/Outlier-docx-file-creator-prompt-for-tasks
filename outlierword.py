# Paste your prompt and the criteria given by Vercel to the app,
# copy and paste "final_prompt.txt" to the ChatGPT,
# and your prompt constraints file is ready.
# pip install kivy (for Mac)

import os
import re
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

KV = '''
<MainWidget>:
    orientation: 'vertical'
    padding: 10
    spacing: 10

    Label:
        text: '1) Prompt metnini girin (cümlelere ayrılacak):'
        size_hint_y: None
        height: self.texture_size[1]

    TextInput:
        id: prompt_input
        multiline: True
        size_hint_y: None
        height: 150

    Label:
        text: '2) İlk grup kriterler (Instruction Following):'
        size_hint_y: None
        height: self.texture_size[1]

    TextInput:
        id: criteria1_input
        multiline: False
        size_hint_y: None
        height: 40

    Label:
        text: '3) İkinci grup kriterler (Accuracy):'
        size_hint_y: None
        height: self.texture_size[1]

    TextInput:
        id: criteria2_input
        multiline: False
        size_hint_y: None
        height: 40

    Button:
        text: 'final_prompt.txt Oluştur'
        size_hint_y: None
        height: 50
        on_press: root.generate_prompt_file()
'''

class MainWidget(BoxLayout):
    def generate_prompt_file(self):
        # 1) Girdileri oku
        prompt = self.ids.prompt_input.text.strip()
        crit1  = self.ids.criteria1_input.text.strip()
        crit2  = self.ids.criteria2_input.text.strip()

        # 2) Cümlelere ayır (isterseniz sonradan ChatGPT'de de kullanabilirsiniz)
        sentences = [s for s in re.split(r'(?<=[\.\!\?])\s+', prompt) if s]

        # 3) final_prompt metnini hazırla
        final_prompt_lines = []
        final_prompt_lines.append(
            'Separate this prompt to sentence by sentence and write each sentence '
            'to the word file with 3 columns named "sentence", "Instruction following" and "accuracy":'
        )
        final_prompt_lines.append(prompt)
        final_prompt_lines.append('')
        final_prompt_lines.append(
            'I will send you criteria as 2 parts, you will match each sentence in these 2 group criteria '
            'with the sentences you made apart in the prompt I gave you. You will place the criteria in the '
            'first group to the Instruction Following column and for 2nd group to the accuracy column.'
        )
        final_prompt_lines.append('')
        final_prompt_lines.append(f'Criteria Group 1 (Instruction Following): {crit1}')
        final_prompt_lines.append(f'Criteria Group 2 (Accuracy): {crit2}')
        final_prompt_lines.append('Give me a docx file, Start with a bold header in the middle of the line which is "Mandolin March Constraint Creation". After that Write a "Prompt" header and paste the prompt and finally add a Constraints header and table with 3 column.')

        final_prompt = '\n'.join(final_prompt_lines)

        # 4) Dosya yolunu oluştur ve yaz
        out_path = 'final_prompt.txt'
        # Eğer klasör gerekiyorsa diye kontrol edebilirsiniz:
        # os.makedirs(os.path.dirname(out_path), exist_ok=True)

        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(final_prompt)

        # 5) Bildirim popup'u
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        popup = Popup(
            title='Tamamlandı',
            content=Label(text=f'“{out_path}” oluşturuldu.'),
            size_hint=(None,None), size=(400,200)
        )
        popup.open()

class PromptApp(App):
    def build(self):
        Builder.load_string(KV)
        return MainWidget()

if __name__ == '__main__':
    PromptApp().run()
