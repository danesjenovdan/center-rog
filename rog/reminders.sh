echo "run the reminders"
python manage.py user_event_reminder|| :
python manage.py user_fee_expiration_reminder|| :
python manage.py membership_expiration_reminder || :
echo "reminders done"
