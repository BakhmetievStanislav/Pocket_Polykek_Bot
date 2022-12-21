import http.client
import json

def get_group_id_by_name(group_number: str) -> int:
    server_address = 'ruz.spbstu.ru'
    request = f'/api/v1/ruz/search/groups?&q={group_number}'

    try:
        connection = http.client.HTTPSConnection(server_address)
        connection.request('GET', request)
        response = connection.getresponse()
        ans = response.read()
        connection.close()

        ans_dict = json.loads(ans)

        if ans_dict['groups'][0]['name'] == group_number:
            return ans_dict['groups'][0]['id']
        else:
            return ans_dict['groups'][1]['id']
    except:
        return -1

def get_schedule_dict_by_id_and_date(group_id: int, date: str):
    date = date.replace('.', '-')
    server_address = 'ruz.spbstu.ru'
    request = f'https://ruz.spbstu.ru/api/v1/ruz/scheduler/{group_id}?date={date}'

    try:
        connection = http.client.HTTPSConnection(server_address)
        connection.request('GET', request)
        response = connection.getresponse()
        ans = response.read()
        connection.close()

        ans_dict = json.loads(ans)

        return ans_dict
    except:
        return -1

class Lesson:
    def __init__(
            self,
            subject: str,
            time_start: str,
            time_end: str,
            typeObj: str,
            teacher: str,
            place: str
    ):
        self.subject = subject
        self.time_start = time_start
        self.time_end = time_end
        self.typeObj = typeObj
        self.teacher = teacher
        self.place = place

    def __str__(self):
        subject_line = f'{self.subject} ({self.typeObj})'
        time_line = f'{self.time_start}-{self.time_end}'
        teacher_line = f'{self.teacher}'
        place_line = f'{self.place}'

        lesson = f'{time_line} {subject_line}\n{teacher_line}\n{place_line}\n\n'

        return lesson

def lesson_from_dict(dict: dict, date: str) -> str:
    schedule = 'В этот день вам не нужно идти на пары!'
    try:
        for day in dict["days"]:
            if date.split('.')[2] in day["date"].split('-')[2]:
                schedule = f'***{day["date"]}***\n\n'
                for lesson in day["lessons"]:
                    try:
                        subject = lesson["subject"]
                    except:
                        subject = f"Изучение темной стороны силы \U0001F608"
                    try:
                        time_start = lesson["time_start"]
                        time_end = lesson["time_end"]
                    except:
                        time_start = f"\U0001F608 00:00"
                        time_end = f"23:59 \U0001F608"
                    try:
                        typeObj = lesson["typeObj"]["name"]
                    except:
                        typeObj = f"Что-то очень интересное \U0001F608"
                    try:
                        teacher = lesson["teachers"][0]["full_name"]
                    except:
                        teacher = f"Дарт-Вейдер \U0001F608"
                    try:
                        place = f'{lesson["auditories"][0]["building"]["name"]}, ауд. {lesson["auditories"][0]["name"]}'
                    except:
                        place = f"Звезда смерти \U0001F608"

                    lesson_str = Lesson(
                        subject=subject,
                        time_start=time_start,
                        time_end=time_end,
                        typeObj=typeObj,
                        teacher=teacher,
                        place=place
                    )

                    schedule += str(lesson_str)

                break
    except:
        schedule = 'В это день вам не нужно идти на пары!'

    return schedule


