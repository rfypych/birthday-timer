# Birthday Reminder Application

This birthday reminder application is specially designed to record and remind you of the birthdays of special people in your life. With an attractive pixel art style interface and automatic notifications, this application ensures you never forget to send your wishes to your loved ones.

## ✨ Main Features

- **Pixel Art Style Interface**: Attractive user interface with cute pixel art design
- **Notification Reminders**: Automatic notifications for upcoming birthdays (7 days in advance)
- **Birthday Calendar**: Visualization of birthdays in a monthly calendar view
- **Animated Display**: Animated application title and real-time date display
- **Data Management**: Easily add, edit, and delete birthday data
- **Birthday Priority**: Mark important birthdays with high priority status
- **Custom Notification Time**: Set specific times for birthday notifications
- **Backup & Restore**: Export and import birthday data for backup
- **Autostart**: Option to run the application automatically at Windows startup

## 🔧 Additional Features

- **Display Management**: Different colors for today's birthdays, this week's birthdays, and priority birthdays
- **Automatic Calculation**: Automatically calculate age and remaining days
- **Settings Tab**: Easy-to-use settings interface
- **Special Emojis**: Special emojis for high-priority notifications

## 📋 How to Use

1. **Add Birthday**:
   - Enter name, date of birth, notification time, and priority status
   - Click "Save" to add to the database

2. **Edit/Delete Birthday**:
   - Select data from the table and click "Edit" or "Delete"
   - For editing, change the necessary information and save changes

3. **View Calendar**:
   - Open the "Calendar" tab to see the monthly calendar view
   - Birthdays are displayed in different colors on the calendar

4. **Backup/Restore Data**:
   - Use the "Export Data" button to save a backup
   - Use the "Import Data" button to restore from a backup

5. **Startup Settings**:
   - Click "Run at Startup" to enable/disable autostart

## 🛠️ Technical

### Requirements

```
pillow==10.2.0
win10toast==0.9
tkcalendar==1.6.1
pywin32==306
```

### Installation

1. Make sure Python 3.7+ is installed on your system
2. Install required packages: `pip install -r requirements.txt`
3. Run the application: `python app.py`

### File Structure

- `app.py`: Main application file
- `birthdays.json`: Birthday database (created automatically)
- `cake_icon.ico`: Application icon (optional)

## ⚠️ Attention

This application is made specifically for personal use. Do not distribute it without permission. Please contact the developer if you need support or have questions.

## 📝 Version Notes

**Version 2.0:**
- Added birthday priority feature
- Added custom notification time settings
- Added settings tab
- Added data export/import feature
- Added UI animation and real-time display
- Improved notification system
- Overall improvements to display and usability

**Version 1.0:**
- Initial release with basic birthday reminder features

---

Made with ❤️ for Someone
