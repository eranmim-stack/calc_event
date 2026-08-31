import tkinter as tk
from tkinter import ttk, messagebox

def calculate():
    try:
        # 1. סוג לקוח (הנחת מוסד/בית ספר 10%)
        is_school = client_type_var.get() == "school"

        # 2. מרחק ונסיעות
        travel_index = travel_combo.current()
        travel_cost = 0
        travel_name = "מקומי / קרוב"
        if travel_index == 1:
            travel_cost = 500
            travel_name = "מרחק בינוני (עד שעה נסיעה)"
        elif travel_index == 2:
            travel_cost = 1000
            travel_name = "מרוחק (עד שעה וחצי נסיעה)"

        # 3. חבילת בסיס - 3,200 ש"ח
        base_price = 3200

        # 4. שעות חזרה גנרלית / המתנה (350 ש"ח לשעה)
        extra_hours = int(hours_spin.get() or 0)
        extra_hours_price = extra_hours * 350

        # 5. מיקרופונים אלחוטיים (2 כלולים בבסיס, 150 ש"ח לכל נוסף)
        total_mics = int(mics_spin.get() or 2)
        extra_mics = max(0, total_mics - 2)
        mics_price = extra_mics * 150

        # 6. תאורה
        light_basic = light_basic_var.get()
        light_truss = light_truss_var.get()
        light_follow = light_follow_var.get()
        lighting_price = (600 if light_basic else 0) + (1400 if light_truss else 0) + (650 if light_follow else 0)

        # 7. וידאו ומסכים
        projector = projector_var.get()
        led_screens = led_screens_var.get()
        video_price = (500 if projector else 0) + (1000 if led_screens else 0)

        # 8. שירותי DJ
        dj_service = dj_var.get()
        dj_price = 1000 if dj_service else 0

        # 9. להקה / מוניטורים
        has_band = band_var.get()
        band_price = 1200 if has_band else 0

        extra_monitors = int(monitors_spin.get() or 0)
        monitors_price = extra_monitors * 150

        # 10. הקמה מוקדמת (הפרדה בין מקומי לחוץ/מרוחק)
        early_local_price = 400 if early_local_var.get() else 0
        early_out_price = 600 if early_out_var.get() else 0
        total_early_price = early_local_price + early_out_price

        # חישוב סכומים
        subtotal = (base_price + travel_cost + extra_hours_price + mics_price + 
                    lighting_price + video_price + dj_price + band_price + monitors_price + total_early_price)
        
        discount = subtotal * 0.10 if is_school else 0
        final_before_vat = subtotal - discount
        vat = final_before_vat * 0.18
        final_with_vat = final_before_vat + vat

        # תצוגת פירוט (מיושרת לימין)
        res_text = "פירוט הצעת מחיר - חבילת בסיס + תוספות:\n"
        res_text += "----------------------------------------------\n"
        res_text += f"• חבילת בסיס (PA, מיקסר, מוניטור, 2 אלחוטיים, צוות 2 אנשים, עד 3 שעות): {base_price:,} ש\"ח\n"
        if travel_cost > 0:
            res_text += f"• תוספת נסיעות ({travel_name}): {travel_cost:,} ש\"ח\n"
        if extra_hours > 0:
            res_text += f"• חזרה גנרלית / שעות נוספות ({extra_hours} שעות): {extra_hours_price:,} ש\"ח\n"
        if extra_mics > 0:
            res_text += f"• תוספת מיקרופונים אלחוטיים ({extra_mics} יח' מעבר לבסיס): {mics_price:,} ש\"ח\n"
        if extra_monitors > 0:
            res_text += f"• תוספת מוניטורים לבמה ({extra_monitors} יח'): {monitors_price:,} ש\"ח\n"
        if dj_price > 0:
            res_text += f"• שירותי DJ / מוסיקה למופע ולמסיבה: {dj_price:,} ש\"ח\n"
        if lighting_price > 0:
            res_text += f"• תאורה / גשרים / פולו-ספוט: {lighting_price:,} ש\"ח\n"
        if video_price > 0:
            res_text += f"• מקרן / מסכי LED: {video_price:,} ש\"ח\n"
        if band_price > 0:
            res_text += f"• חיבור להקה / נגנים: {band_price:,} ש\"ח\n"
        if early_local_price > 0:
            res_text += f"• פיצול יום / הקמה מוקדמת (אירוע מקומי): {early_local_price:,} ש\"ח\n"
        if early_out_price > 0:
            res_text += f"• הקמה מוקדמת / שהייה (אירוע חוץ/מרוחק): {early_out_price:,} ש\"ח\n"

        res_text += "-" * 40 + "\n"
        res_text += f"סה\"כ מחירון: {subtotal:,.0f} ש\"ח\n"
        if is_school:
            res_text += f"הנחת מוסד / בית ספר (10%): -{discount:,.0f} ש\"ח\n"

        res_text += "=" * 40 + "\n"
        res_text += f"מחיר לפני מע\"מ: {final_before_vat:,.0f} ש\"ח\n"
        res_text += f"מע\"מ (18%): {vat:,.0f} ש\"ח\n"
        res_text += f"סה\"כ כולל מע\"מ: {final_with_vat:,.0f} ש\"ח"

        result_text_box.config(state="normal")
        result_text_box.delete("1.0", tk.END)
        result_text_box.insert(tk.END, res_text)
        result_text_box.config(state="disabled")

    except ValueError:
        messagebox.showerror("שגיאה", "אנא הזן מספרים תקינים")

# חלון ראשי
root = tk.Tk()
root.title("מחשבון תמחור אירועים - עירן מימוני")
root.geometry("520x800")

title = tk.Label(root, text="מחשבון תמחור הגברה, תאורה ווידאו", font=("Arial", 15, "bold"))
title.pack(pady=8)

# סוג לקוח ונסיעות
frame_top = tk.LabelFrame(root, text=" כללי ונסיעות ", font=("Arial", 10, "bold"))
frame_top.pack(fill="x", padx=12, pady=4)

client_type_var = tk.StringVar(value="regular")
tk.Radiobutton(frame_top, text="לקוח רגיל / פרטי", variable=client_type_var, value="regular").pack(anchor="e", padx=10)
tk.Radiobutton(frame_top, text="בית ספר / מוסד (10% הנחה)", variable=client_type_var, value="school").pack(anchor="e", padx=10)

tk.Label(frame_top, text=":מרחק הגעה").pack(anchor="e", padx=10, pady=(4,0))
travel_combo = ttk.Combobox(frame_top, values=["מקומי / קרוב (0 ש\"ח)", "מרחק בינוני - עד שעה (+500 ש\"ח)", "מרוחק - עד שעה וחצי (+1,000 ש\"ח)"], state="readonly", justify="right")
travel_combo.current(0)
travel_combo.pack(fill="x", padx=10, pady=2)

# חבילת בסיס ושעות
frame_base = tk.LabelFrame(root, text=" חבילת בסיס ושעות ", font=("Arial", 10, "bold"))
frame_base.pack(fill="x", padx=12, pady=4)

tk.Label(frame_base, text="חבילת בסיס: 3,200 ש\"ח (PA, מיקסר, מוניטור, 2 אלחוטיים, צוות 2 אנשים, עד 3 שעות)", font=("Arial", 9, "italic"), fg="#333333").pack(anchor="e", padx=10, pady=2)

f_hours = tk.Frame(frame_base)
f_hours.pack(fill="x", padx=10, pady=4)
hours_spin = tk.Spinbox(f_hours, from_=0, to=12, width=4)
hours_spin.pack(side="left")
tk.Label(f_hours, text=":שעות חזרה גנרלית / המתנה נוספות (350 ש\"ח/שעה)").pack(side="right")

# ציוד ותוספות
frame_addons = tk.LabelFrame(root, text=" ציוד ותוספות ", font=("Arial", 10, "bold"))
frame_addons.pack(fill="x", padx=12, pady=4)

f_mics = tk.Frame(frame_addons)
f_mics.pack(fill="x", padx=10, pady=2)
mics_spin = tk.Spinbox(f_mics, from_=2, to=20, width=4)
mics_spin.pack(side="left")
tk.Label(f_mics, text=":סה\"כ מיקרופונים אלחוטיים (2 כלולים בבסיס, 150 ש\"ח לכל נוסף)").pack(side="right")

f_monitors = tk.Frame(frame_addons)
f_monitors.pack(fill="x", padx=10, pady=2)
monitors_spin = tk.Spinbox(f_monitors, from_=0, to=10, width=4)
monitors_spin.pack(side="left")
tk.Label(f_monitors, text=":תוספת מוניטורים לבמה (1 כלול בבסיס, 150 ש\"ח לכל נוסף)").pack(side="right")

dj_var = tk.BooleanVar()
tk.Checkbutton(frame_addons, text="תוספת שירותי DJ / מוסיקה למופע (1,000 ש\"ח)", variable=dj_var).pack(anchor="e", padx=10)

projector_var = tk.BooleanVar()
tk.Checkbutton(frame_addons, text="מקרן + מסך (500 ש\"ח)", variable=projector_var).pack(anchor="e", padx=10)

led_screens_var = tk.BooleanVar()
tk.Checkbutton(frame_addons, text="2 מסכי LED 65 אינץ' על סטנדים (1,000 ש\"ח)", variable=led_screens_var).pack(anchor="e", padx=10)

light_basic_var = tk.BooleanVar()
tk.Checkbutton(frame_addons, text="תאורת במה בסיסית - 8 פנסים (600 ש\"ח)", variable=light_basic_var).pack(anchor="e", padx=10)

light_truss_var = tk.BooleanVar()
tk.Checkbutton(frame_addons, text="גשר תאורה (1,400 ש\"ח)", variable=light_truss_var).pack(anchor="e", padx=10)

light_follow_var = tk.BooleanVar()
tk.Checkbutton(frame_addons, text="פולו ספוט + מפעיל ייעודי (650 ש\"ח)", variable=light_follow_var).pack(anchor="e", padx=10)

band_var = tk.BooleanVar()
tk.Checkbutton(frame_addons, text="חיבור להקה / נגנים (1,200 ש\"ח)", variable=band_var).pack(anchor="e", padx=10)

early_local_var = tk.BooleanVar()
tk.Checkbutton(frame_addons, text="פיצול יום / הקמה מוקדמת - אירוע מקומי (400 ש\"ח)", variable=early_local_var).pack(anchor="e", padx=10)

early_out_var = tk.BooleanVar()
tk.Checkbutton(frame_addons, text="הקמה מוקדמת / שהייה ארוכה - אירוע חוץ/מרוחק (600 ש\"ח)", variable=early_out_var).pack(anchor="e", padx=10)

# כפתור חישוב
btn_calc1 = tk.Button(root, text="חשב הצעת מחיר", command=calculate, bg="#1976D2", fg="white", font=("Arial", 11, "bold"))
btn_calc1.pack(fill="x", padx=12, pady=6)

# אזור תוצאות
frame_res = tk.Frame(root)
frame_res.pack(fill="both", expand=True, padx=12, pady=5)

scrollbar = tk.Scrollbar(frame_res)
scrollbar.pack(side="left", fill="y")

result_text_box = tk.Text(frame_res, yscrollcommand=scrollbar.set, font=("Arial", 10), height=8, bg="#f8f9fa", state="disabled", wrap="none")
result_text_box.pack(side="right", fill="both", expand=True)
result_text_box.tag_configure("right", justify="right")
scrollbar.config(command=result_text_box.yview)

root.mainloop()