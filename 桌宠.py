from tkinter import HIDDEN, NORMAL, DISABLED, Tk, Canvas, Button, messagebox
import time

class PetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("桌宠")

        self.canvas_width = 1000
        self.canvas_height = 800

        self.c = Canvas(root, width=self.canvas_width, height=self.canvas_height)
        self.c.configure(bg='dark blue', highlightthickness=0)
        self.c.pack()

        self.c.body_color = 'SkyBlue1'
        color = self.c.body_color

        self.body = self.c.create_oval(35, 20, 365, 350, outline=color, fill=color)
        self.ear_left = self.c.create_polygon(75, 80, 75, 10, 165, 70, outline=color, fill=color)
        self.ear_right = self.c.create_polygon(255, 45, 325, 10, 320, 70, outline=color, fill=color)
        self.foot_left = self.c.create_oval(65, 320, 145, 360, outline=color, fill=color)
        self.foot_right = self.c.create_oval(250, 320, 330, 360, outline=color, fill=color)
        self.eye_left = self.c.create_oval(130, 110, 160, 170, outline='black', fill='white')
        self.eye_right = self.c.create_oval(230, 110, 260, 170, outline='black', fill='white')
        self.pupil_left = self.c.create_oval(140, 145, 150, 155, outline='black', fill='black')
        self.pupil_right = self.c.create_oval(240, 145, 250, 155, outline='black', fill='black')
        self.mouth_normal = self.c.create_line(170, 250, 200, 272, 230, 250, smooth=1, width=2, state=NORMAL)
        self.mouth_happy = self.c.create_line(170, 250, 200, 282, 230, 250, smooth=1, width=2, state=HIDDEN)
        self.mouth_sad = self.c.create_line(170, 250, 200, 232, 230, 250, smooth=1, width=2, state=HIDDEN)
        self.tongue_main = self.c.create_rectangle(170, 250, 230, 290, outline='red', fill='red', state=HIDDEN)
        self.tongue_tip = self.c.create_oval(170, 285, 230, 300, outline='red', fill='red', state=HIDDEN)
        self.cheek_left = self.c.create_oval(70, 180, 120, 230, outline='pink', fill='pink', state=HIDDEN)
        self.cheek_right = self.c.create_oval(280, 180, 330, 230, outline='pink', fill='pink', state=HIDDEN)

        self.feed_button = Button(root, text="喂我", width=80, height=3, command=self.feed_pet, background='SkyBlue1', fg='black')
        self.feed_button.pack()

        self.clean_button = Button(root, text="还没有粑粑", width=80, height=3, state=DISABLED, command=self.clean_poop, background='SkyBlue1', fg='black')
        self.clean_button.pack()

        self.c.bind('<Motion>', self.show_happy)
        self.c.bind('<Leave>', self.hide_happy)
        self.c.bind('<Double-1>', self.cheeky)

        self.c.happy_level = 10
        self.c.eye_crossed = False
        self.c.tongue_out = False
        self.is_eating = False
        self.has_pooped = False
        self.last_fed_time = time.time()

        self.root.after(1000, self.blink)
        self.root.after(5000, self.sad)
        self.root.after(3600000, self.sleep)  # 每小时睡一次
        self.root.after(60000, self.check_hunger)  # 每分钟检查一次饥饿状态

        self.center_pet()
        def About():
            messagebox.showinfo('关于', '关于‘桌宠’\nBeta 0.1\n更多信息请前往网站查看')
    
        about = Button(root, text='关于', width=80, height=3, command=About, bg='SkyBlue1', fg='black')
        about.pack()
        

    def center_pet(self):
        pet_coords = self.c.bbox(self.body)
        pet_center_x = (pet_coords[0] + pet_coords[2]) // 2
        pet_center_y = (pet_coords[1] + pet_coords[3]) // 2
        canvas_center_x = self.canvas_width // 2
        canvas_center_y = self.canvas_height // 2
        offset_x = canvas_center_x - pet_center_x
        offset_y = canvas_center_y - pet_center_y
        self.c.move(self.body, offset_x, offset_y)
        self.c.move(self.ear_left, offset_x, offset_y)
        self.c.move(self.ear_right, offset_x, offset_y)
        self.c.move(self.foot_left, offset_x, offset_y)
        self.c.move(self.foot_right, offset_x, offset_y)
        self.c.move(self.eye_left, offset_x, offset_y)
        self.c.move(self.eye_right, offset_x, offset_y)
        self.c.move(self.pupil_left, offset_x, offset_y)
        self.c.move(self.pupil_right, offset_x, offset_y)
        self.c.move(self.mouth_normal, offset_x, offset_y)
        self.c.move(self.mouth_happy, offset_x, offset_y)
        self.c.move(self.mouth_sad, offset_x, offset_y)
        self.c.move(self.tongue_main, offset_x, offset_y)
        self.c.move(self.tongue_tip, offset_x, offset_y)
        self.c.move(self.cheek_left, offset_x, offset_y)
        self.c.move(self.cheek_right, offset_x, offset_y)

    def blink(self):
        self.toggle_eyes()
        self.root.after(250, self.toggle_eyes)
        self.root.after(3000, self.blink)

    def toggle_eyes(self):
        current_color = self.c.itemcget(self.eye_left, 'fill')
        new_color = self.c.body_color if current_color == 'white' else 'white'
        current_state = self.c.itemcget(self.pupil_left, 'state')
        new_state = NORMAL if current_state == HIDDEN else HIDDEN
        self.c.itemconfigure(self.pupil_left, state=new_state)
        self.c.itemconfigure(self.pupil_right, state=new_state)
        self.c.itemconfigure(self.eye_left, fill=new_color)
        self.c.itemconfigure(self.eye_right, fill=new_color)

    def toggle_pupils(self):
        if not self.c.eye_crossed:
            self.c.move(self.pupil_left, 10, -5)
            self.c.move(self.pupil_right, -10, -5)
            self.c.eye_crossed = True
        else:
            self.c.move(self.pupil_left, -10, 5)
            self.c.move(self.pupil_right, 10, 5)
            self.c.eye_crossed = False

    def toggle_tongue(self):
        if not self    .c.tongue_out:
            self.c.itemconfigure(self.tongue_tip, state=NORMAL)
            self.c.itemconfigure(self.tongue_main, state=NORMAL)
            self.c.tongue_out = True
        else:
            self.c.itemconfigure(self.tongue_tip, state=HIDDEN)
            self.c.itemconfigure(self.tongue_main, state=HIDDEN)
            self.c.tongue_out = False

    def cheeky(self, event):
        self.toggle_tongue()
        self.toggle_pupils()
        self.hide_happy(event)
        self.root.after(1000, self.toggle_tongue)
        self.root.after(1000, self.toggle_pupils)
        return

    def show_happy(self, event):
        if (20 <= event.x <= 350) and (20 <= event.y <= 350):
            self.c.itemconfigure(self.cheek_left, state=NORMAL)
            self.c.itemconfigure(self.cheek_right, state=NORMAL)
            self.c.itemconfigure(self.mouth_happy, state=NORMAL)
            self.c.itemconfigure(self.mouth_normal, state=HIDDEN)
            self.c.itemconfigure(self.mouth_sad, state=HIDDEN)
        return

    def hide_happy(self, event):
        self.c.itemconfigure(self.cheek_left, state=HIDDEN)
        self.c.itemconfigure(self.cheek_right, state=HIDDEN)
        self.c.itemconfigure(self.mouth_happy, state=HIDDEN)
        self.c.itemconfigure(self.mouth_normal, state=NORMAL)
        self.c.itemconfigure(self.mouth_sad, state=HIDDEN)
        return

    def sad(self):
        if self.c.happy_level == 0:
            self.c.itemconfigure(self.mouth_happy, state=HIDDEN)
            self.c.itemconfigure(self.mouth_normal, state=HIDDEN)
            self.c.itemconfigure(self.mouth_sad, state=NORMAL)
        else:
            self.c.happy_level -= 1
        self.root.after(5000, self.sad)

    def feed_pet(self):
        if not self.is_eating:
            self.is_eating = True
            self.feed_button.config(text="宠物正在吃饭", state=DISABLED)
            self.root.after(30000, self.finish_eating)
            self.c.happy_level += 10
            self.grow_pet()

    def finish_eating(self):
        self.feed_button.config(text="宠物正在拉粑粑", state=DISABLED)
        self.root.after(20000, self.finish_poop)
        self.last_fed_time = time.time()
        self.is_eating = False
    
   

    def finish_poop(self):
        self.feed_button.config(text="喂我", state=DISABLED)
        self.clean_button.config(text="清理粑粑", state=NORMAL)
        self.has_pooped = True
        self.show_poop()

    def clean_poop(self):
        self.clean_button.config(text="还没有粑粑", state=DISABLED)
        self.feed_button.config(state=NORMAL)
        self.has_pooped = False
        self.hide_poop()

    def show_poop(self):
        if self.has_pooped:
            poop_color = 'brown'  
            poop_coords = self.c.coords(self.body)  
            poop_center_x = (poop_coords[0] + poop_coords[2]) // 2  
            poop_bottom_y = poop_coords[3] + 20  
            poop_size = 20  
            self.poop = self.c.create_oval(poop_center_x - poop_size, poop_bottom_y - poop_size, poop_center_x + poop_size, poop_bottom_y + poop_size, fill=poop_color)

    def hide_poop(self):
        if hasattr(self, 'poop'):
            self.c.delete(self.poop)

    def check_hunger(self):
        if time.time() - self.last_fed_time > 1800:  
            self.reset_size()
        self.root.after(60000, self.check_hunger)

    def grow_pet(self):
        self.c.scale(self.body, 200, 200, 1.1, 1.1)
        self.c.scale(self.ear_left, 200, 200, 1.1, 1.1)
        self.c.scale(self.ear_right, 200, 200, 1.1, 1.1)
        self.c.scale(self.foot_left, 200, 200, 1.1, 1.1)
        self.c.scale(self.foot_right, 200, 200, 1.1, 1.1)
        self.c.scale(self.eye_left, 200, 200, 1.1, 1.1)
        self.c.scale(self.eye_right, 200, 200, 1.1, 1.1)
        self.c.scale(self.pupil_left, 200, 200, 1.1, 1.1)
        self.c.scale(self.pupil_right, 200, 200, 1.1, 1.1)
        self.c.scale(self.mouth_normal, 200, 200, 1.1, 1.1)
        self.c.scale(self.mouth_happy, 200, 200, 1.1, 1.1)
        self.c.scale(self.mouth_sad, 200, 200, 1.1, 1.1)
        self.c.scale(self.tongue_main, 200, 200, 1.1, 1.1)
        self.c.scale(self.tongue_tip, 200, 200, 1.1, 1.1)
        self.c.scale(self.cheek_left, 200, 200, 1.1, 1.1)
        self.c.scale(self.cheek_right, 200, 200, 1.1, 1.1)

    def reset_size(self):
        self.c.scale(self.body, 200, 200, 1 / 1.1, 1 / 1.1)
        self.c.scale(self.ear_left, 200, 200, 1 / 1.1, 1 / 1.1)
        self.c.scale(self.ear_right, 200, 200, 1 / 1.1, 1 / 1.1)
        self.c.scale(self.foot_left, 200, 200, 1 / 1.1, 1 / 1.1)
        self.c.scale(self.foot_right, 200, 200, 1 / 1.1, 1 / 1.1)
        self.c.scale(self.eye_left, 200, 200, 1 / 1.1, 1 / 1.1)
        self.c.scale(self.eye_right, 200, 200, 1 / 1.1, 1 / 1.1)
        self.c.scale(self.pupil_left, 200, 200, 1 / 1.1, 1 / 1.1)
        self.c.scale(self.pupil_right, 200, 200, 1 / 1.1, 1 / 1.1)
        self.c.scale(self.mouth_normal, 200, 200, 1 / 1.1, 1 / 1.1)
        self.c.scale(self.mouth_happy, 200, 200, 1 / 1.1, 1 / 1.1)
        self.c.scale(self.mouth_sad, 200, 200, 1 / 1.1, 1 / 1.1)
        self.c.scale(self.tongue_main, 200, 200, 1 / 1.1, 1 / 1.1)
        self.c.scale(self.tongue_tip, 200, 200, 1 / 1.1, 1 / 1.1)
        self.c.scale(self.cheek_left, 200, 200, 1 / 1.1, 1 / 1.1)

    def sleep(self):
        self.feed_button.config(text="宠物正在睡觉，无法与其互动", state=DISABLED)
        self.clean_button.config(state=DISABLED)
        self.root.after(1200000, self.wake_up)  # 20分钟后醒来

    def wake_up(self):
        self.feed_button.config(text="喂我", state=NORMAL)
        self.clean_button.config(state=DISABLED)

root = Tk()
exit = Button(root, text='退出', width=80, height=3, command=root.destroy, bg='SkyBlue1', fg='black')
exit.pack()
app = PetApp(root)
root.mainloop()
    


