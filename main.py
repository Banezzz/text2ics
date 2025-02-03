#!/usr/bin/env python3
import re
from datetime import datetime
import uuid

def generate_ics(events):
    ics_lines = []
    ics_lines.append("BEGIN:VCALENDAR")
    ics_lines.append("VERSION:2.0")
    ics_lines.append("PRODID:-//Calendar Converter//EN")
    for event in events:
        ics_lines.append("BEGIN:VEVENT")
        # 生成一个随机 UID
        uid = str(uuid.uuid4())
        ics_lines.append(f"UID:{uid}")
        # 记录生成事件的时间戳，使用 UTC 时间
        dtstamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        ics_lines.append(f"DTSTAMP:{dtstamp}")
        # 直接用原文作为 SUMMARY
        ics_lines.append(f"SUMMARY:{event['summary']}")
        if event["all_day"]:
            # 全日事件格式（日期值格式）
            ics_lines.append(f"DTSTART;VALUE=DATE:{event['dtstart']}")
            ics_lines.append(f"DTEND;VALUE=DATE:{event['dtend']}")
        else:
            # 定时事件，设定时区为 Asia/Shanghai （UTC+8）
            ics_lines.append(f"DTSTART;TZID=Asia/Shanghai:{event['dtstart']}")
            ics_lines.append(f"DTEND;TZID=Asia/Shanghai:{event['dtend']}")
        ics_lines.append("END:VEVENT")
    ics_lines.append("END:VCALENDAR")
    return "\n".join(ics_lines)

def parse_file(filepath):
    events = []
    in_tbd_section = False
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 判断 TBD 区段标记
            if "TBD in February" in line:
                in_tbd_section = True
                continue
            # TBD 区段内仅处理以 '$' 开头的行
            if in_tbd_section:
                if line.startswith("$"):
                    event = {
                        "summary": line,
                        # 全月事件：使用 all-day 格式，从 2025-02-01 到 2025-03-01 不含结束日
                        "dtstart": "20250201",
                        "dtend": "20250301",
                        "all_day": True
                    }
                    events.append(event)
                continue
            # 处理含有具体日期的活动（匹配 "Feb X:" 或 "~Feb X:"）
            match = re.match(r"^~?\s*Feb\s+(\d+):", line)
            if match:
                day = match.group(1).zfill(2)
                # 格式化为 ICS 标准（YYYYMMDDTHHMMSS），这里定在上午 9:00 到 10:00
                start_str = f"202502{day}T090000"
                end_str = f"202502{day}T100000"
                event = {
                    "summary": line,
                    "dtstart": start_str,
                    "dtend": end_str,
                    "all_day": False
                }
                events.append(event)
    return events

def main():
    input_filename = "input.txt"
    output_filename = "output.ics"
    events = parse_file(input_filename)
    ics_content = generate_ics(events)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(ics_content)
    print("ICS 文件已生成：", output_filename)

if __name__ == "__main__":
    main()
