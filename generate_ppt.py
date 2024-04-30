class generate_ppt:

    def __init__(self, topic: str) -> None:
        import pptx
        self.topic = topic
        self.presentation = pptx.Presentation('powerpoints/modern_stud_project.pptx')
        self.modern_stud_project()
        
    def get_data(self):
        import google.generativeai as genai
        from dotenv import load_dotenv
        import os

        load_dotenv()

        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-pro')


        prompt = f'Fill the below json with the content of topic: "{self.topic}" in plain text avoid markdown for my ppt'

        json_format = '''
        {
        "slides": [
        {
        "topic": f"{self.topic}"
        },
        {
        "title": "Introduction",
        "content": "{intoduction}"
        },
        {
        "title": "Project Background",
        "content": "{project background}"
        },
        {
        "title": "project objectives",
        "content": ["{objective_1_desc}", "{objective_2_desc}", "{objective_3_desc}"]
        },
        {
        "title": "project methodology",
        "content": ["{methodology_1_desc}","{methodology_2_desc}", "{methodology_3_desc}"]
        },
        {
        "title": "conclusion",
        "content": "{conclusion}"
        }
        ]
        }
        '''

        prompt = prompt + json_format
        response = model.generate_content(prompt)

        print(f'prompt: {prompt}, response: {response.text}')

        import json
        json_response: json = json.loads(response.text)

        with open('slides.json','w') as f:
            json.dump(json_response, f, indent=4)
        
        return json_response


    def list_text_boxes(self, presentation, slide_num):
        slide = presentation.slides[slide_num-1]
        text_boxes = []
        for shape in slide.shapes:
            if shape.has_text_frame and shape.text:
                text_boxes.append(shape.text)
        return text_boxes

    def get_text_box_id(self, slide_no):
        for idx, text in enumerate(self.list_text_boxes('presentation', slide_no), 1):
            print(f"Text Box {idx}: {text}")


    def update_text_of_textbox(self, slide, text_box_id, new_text):
        slide = self.presentation.slides[(slide - 1)]
        count = 0
        for shape in slide.shapes:
            if shape.has_text_frame and shape.text:
                count += 1
                if count == text_box_id:
                    text_frame = shape.text_frame
                    first_paragraph = text_frame.paragraphs[0]
                    first_run = first_paragraph.runs[0] if first_paragraph.runs else first_paragraph.add_run()
                    first_run.text = new_text
                    return
        raise ValueError(f"Slide {slide} or Text Box ID {text_box_id} not found")

    def modern_stud_project(self):
        data = self.get_data()
        self.update_text_of_textbox(1,2,data['slides'][0]['topic'])
        self.presentation.save('output/modern_stud_project.pptx')
        print('ppt saved')


    # update_text_of_textbox(presentation,2,2,'Introduction of this prject is this this this')

    # presentation.save('output/modern_stud_project.pptx')


    # result = get_data('AI chatbot')
    # print(result)
    # update_text_of_textbox(presentation,1,2,)

a = generate_ppt('AI Chatbot')