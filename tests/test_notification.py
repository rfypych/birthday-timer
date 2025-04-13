import unittest
from datetime import datetime, timedelta
from ..notification import BirthdayNotifier

class TestNotification(unittest.TestCase):
    """Test case untuk modul notifikasi"""
    
    def setUp(self):
        """Inisialisasi objek notifikasi sebelum setiap test"""
        self.notifier = BirthdayNotifier()
        
    def test_show_notification(self):
        """Test pengiriman notifikasi dasar"""
        result = self.notifier.show_notification(
            title="Test Notifikasi",
            message="Ini adalah test notifikasi",
            duration=2
        )
        # Notifikasi seharusnya berhasil dikirim
        self.assertTrue(result)

    def test_check_birthdays(self):
        """Test pengecekan ulang tahun yang akan datang"""
        # Buat data test
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)
        
        test_birthdays = [
            {
                "id": "1",
                "name": "Test User 1",
                "date": today.strftime("%d/%m/%Y"),
                "time": "00:00"
            },
            {
                "id": "2",
                "name": "Test User 2",
                "date": tomorrow.strftime("%d/%m/%Y"),
                "time": "00:00"
            },
            {
                "id": "3",
                "name": "Test User 3",
                "date": next_week.strftime("%d/%m/%Y"),
                "time": "00:00"
            }
        ]
        
        # Test dengan threshold 7 hari
        notifications = self.notifier.check_birthdays(test_birthdays, days_threshold=7)
        
        # Seharusnya ada 3 notifikasi
        self.assertEqual(len(notifications), 3)
        
        # Cek format notifikasi
        for notif in notifications:
            self.assertIn("title", notif)
            self.assertIn("message", notif)
            self.assertIn("key", notif)

    def test_notification_deduplication(self):
        """Test pencegahan notifikasi duplikat"""
        birthday = {
            "id": "1",
            "name": "Test User",
            "date": datetime.now().strftime("%d/%m/%Y"),
            "time": "00:00"
        }
        
        # Cek pertama kali
        notifications1 = self.notifier.check_birthdays([birthday])
        self.assertEqual(len(notifications1), 1)
        
        # Cek kedua kalinya (seharusnya tidak ada notifikasi karena sudah ditampilkan)
        notifications2 = self.notifier.check_birthdays([birthday])
        self.assertEqual(len(notifications2), 0)
        
        # Reset notifikasi harian
        self.notifier.reset_daily_notifications()
        
        # Cek lagi setelah reset (seharusnya muncul notifikasi)
        notifications3 = self.notifier.check_birthdays([birthday])
        self.assertEqual(len(notifications3), 1)

    def test_invalid_date_format(self):
        """Test penanganan format tanggal yang tidak valid"""
        invalid_birthday = {
            "id": "1",
            "name": "Test User",
            "date": "invalid-date",  # Format tanggal tidak valid
            "time": "00:00"
        }
        
        # Seharusnya tidak ada error, tapi tidak menghasilkan notifikasi
        notifications = self.notifier.check_birthdays([invalid_birthday])
        self.assertEqual(len(notifications), 0)

if __name__ == '__main__':
    unittest.main()