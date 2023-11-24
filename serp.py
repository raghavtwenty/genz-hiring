import serpapi

# Set your SerpApi key
SERP_API_KEY = ""
client = serpapi.Client(api_key=SERP_API_KEY)


def serp_search(Job_Role):
    Job_Role = "Software Developer"
    results = client.search(
        {
            "engine": "google_jobs",
            "q": Job_Role,
            "location": "New York, NY",
            "chips": "date_posted:month",
        }
    )

    for job_result in results["jobs_results"]:
        # Extract details separately
        job_title = job_result.get("title", "N/A")
        company_name = job_result.get("company_name", "N/A")
        location = job_result.get("location", "N/A")
        extensions = job_result.get("extensions", "N/A")
        detected_extensions = job_result.get("detected_extensions", "N/A")

        return (job_title, company_name, location, extensions)

        """
        # Print details
        print(f"Job Title: {job_title}")
        print(f"Company Name: {company_name}")
        print(f"Location: {location}")
        print(f"Extensions: {extensions}")

        """
