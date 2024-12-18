
import re

def normalize_salary(salary):

    if "thoả thuận" in salary.lower():
        return None, None, None
    elif "trên" in salary.lower():
        min_salary = int(re.search(r'\d+', salary).group())
        return min_salary, None, "VND"
    elif "tới" in salary.lower():
        max_salary = int(re.search(r'\d+', salary).group())
        return 0, max_salary, "VND"
    elif "-" in salary:
        match = re.findall(r'\d+', salary)
        if len(match) == 2:  # Đảm bảo có 2 số
            min_salary, max_salary = map(int, match)
            if( "$" in salary):
                return min_salary, max_salary, "USD"
            return min_salary, max_salary, "VND"
        else:
            return None, None, None 
    elif "$" in salary:
        match = re.findall(r'\d+', salary)
        if len(match) == 2:
            min_salary, max_salary = map(int, match)
            return min_salary, max_salary, "USD"
        else:
            return None, None, None  
    return None, None, None


def split_address(address):
    if ':' in address:
        parts = [part.strip() for part in address.split(':')]
    else:
        parts = [part.strip() for part in address.split(',')]

    if len(parts) == 1:
        return None, parts[0]

    if len(parts) == 2:
        district, city = parts[0], parts[1]
        return district, city
    return None, None


def normalize_job_title(job_title):
    title = job_title.lower()

    title = re.sub(r"(lương.*|từ \d+.*|(\d+ năm|năm kinh nghiệm).*|thu nhập từ.*|tới \d+.*|salary.*|code: \w+)", "", title, flags=re.IGNORECASE).strip()
    title = re.sub(r"[\(\)\[\]\{\}]", "", title)  
    title = re.sub(r"\s{2,}", " ", title)  

    if any(keyword in title for keyword in ["intern", "thực tập", "internship"]):
        return "Intern"
    
    if any(keyword in title for keyword in ["developer", "lập trình", "angular", "full-stack", "java", "python", "backend", "frontend"]):
        return "Developer"
    elif any(keyword in title for keyword in ["analyst", "business analyst", "data analyst", "intelligence", "ba"]):
        return "Analyst"
    elif any(keyword in title for keyword in ["support", "helpdesk", "infra", "technical support"]):
        return "IT Support"
    elif any(keyword in title for keyword in ["manager", "project manager", "product manager", "scrum", "quản lý"]):
        return "Manager"
    elif any(keyword in title for keyword in ["devops", "sre", "site reliability", "quản trị hệ thống"]):
        return "DevOps/SRE"
    elif any(keyword in title for keyword in ["secretary", "assistant"]):
        return "Secretary"
    elif any(keyword in title for keyword in ["engineer", "kỹ sư", "qa", "tester", "automation", "architect"]):
        return "Engineer"
    else:
        return "Other"
