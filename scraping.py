import requests
import csv
import re

def parse_course_description(desc):
    """
    Parse credits, prerequisites, cross-listed courses, and gen ed outcomes from course description.
    """
    # 1. Credits: e.g., (3 crs.)
    credits_match = re.search(r'\(?\s*(\d+)\s*crs?\.?\s*\)?', desc, re.IGNORECASE)
    credits = credits_match.group(1) if credits_match else ""

    # 2. Prerequisites: after "Pre:"
    prereq_match = re.search(r"Pre:\s*(.*?)(?:\.|$)", desc)
    prerequisites = prereq_match.group(1).strip() if prereq_match else ""

    # 3. Cross-listed courses: look for "Cross-listed as (ELE 437)"
    cross_match = re.findall(r'Cross-listed as\s*\((.*?)\)', desc, re.IGNORECASE)
    cross_listed = ", ".join(cross_match) if cross_match else ""

    # 4. Gen Ed outcomes: e.g., (D1)
    gen_ed_matches = re.findall(r'\(([A-Z]\d)\)', desc)
    gen_ed = ", ".join(gen_ed_matches) if gen_ed_matches else ""

    return credits, prerequisites, cross_listed, gen_ed

def fetch_courses_by_prefix(prefix, limit=100):
    """
    Fetch all courses matching a given prefix (e.g., 'CSC') from the URI catalog.
    Returns a list of course dictionaries.
    """
    base_url = "https://uri.kuali.co/api/v1/catalog/search/67d1d5f37a3472af016158a7"
    courses = []
    skip = 0

    while True:
        params = {
            "q": prefix,
            "itemTypes": "courses",
            "limit": limit,
            "skip": skip
        }
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch data: status {response.status_code}")
            break

        data = response.json()  # API returns a list
        if not data:
            break  # No more courses

        for course in data:
            course_code = course.get("code", "")
            if course_code.startswith(prefix):
                desc = course.get("description", "")
                credits, prerequisites, cross_listed, gen_ed = parse_course_description(desc)

                courses.append({
                    "code": course_code,
                    "credits": credits,
                    "prerequisites": prerequisites,
                    # "cross_listed": cross_listed,
                    "gen_ed": gen_ed
                })

        skip += limit  # paginate if necessary

    return courses

def save_courses_to_csv(courses, filename):
    """
    Save a list of course dicts to a CSV file.
    """
    # fieldnames = ["code", "credits", "prerequisites", "cross_listed", "gen_ed"]
    fieldnames = ["code", "credits", "prerequisites", "gen_ed"]
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for course in courses:
            writer.writerow(course)

if __name__ == "__main__":
    major_prefix = "CSC"  # Change to any major prefix
    all_courses = fetch_courses_by_prefix(major_prefix)
    print(f"Fetched {len(all_courses)} courses for {major_prefix}")
    filename = major_prefix + "_courses.csv"
    save_courses_to_csv(all_courses, filename)
    print("Saved to " + filename)
