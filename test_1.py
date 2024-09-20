from zk import ZK, const
from datetime import datetime

# Replace with your device's IP address and port
device_ip = "devhasanhr.zapto.org"
port = 4370

# Create ZK instance
zk = ZK(device_ip, port=port, timeout=5, password=0, force_udp=False, ommit_ping=False)


def filter_in_out(attendance_records):
    in_out_records = {}
    for record in attendance_records:
        if record.user_id not in in_out_records:
            in_out_records[record.user_id] = {"in": record.timestamp, "out": None}
        else:
            in_out_records[record.user_id]["out"] = record.timestamp
    return in_out_records


try:
    # Connect to the device
    conn = zk.connect()
    print("Connected to device")

    # Disable the device to ensure no activity during the process
    conn.disable_device()

    # Get user information
    users = conn.get_users()

    # Create a dictionary to map user IDs to user details
    user_dict = {
        user.user_id: {
            "name": user.name,
            "privilege": "Admin" if user.privilege == const.USER_ADMIN else "User",
            "password": user.password,
            "group_id": user.group_id,
        }
        for user in users
    }

    # Get attendance records
    attendance = conn.get_attendance()

    # Get today's date
    today = datetime.today().date()

    # Filter records for today's date
    todays_attendance = [
        record for record in attendance if record.timestamp.date() == today
    ]

    # Filter in and out records
    in_out_records = filter_in_out(todays_attendance)

    # Print today's attendance records with user details and in/out status
    for user_id, times in in_out_records.items():
        user_details = user_dict.get(
            user_id,
            {
                "name": "Unknown",
                "privilege": "Unknown",
                "password": "Unknown",
                "group_id": "Unknown",
            },
        )
        print(
            f"User ID: {user_id}, User Name: {user_details['name']}, Privilege: {user_details['privilege']}, Password: {user_details['password']}, Group ID: {user_details['group_id']}, In: {times['in']}, Out: {times['out']}"
        )

    # Re-enable the device after processing
    conn.enable_device()

except Exception as e:
    print(f"Process terminated: {e}")

finally:
    if conn:
        conn.disconnect()
        print("Disconnected from device")
