# NenAI Workflow Test Prompts

This document contains 10 carefully designed workflow prompts to test the NenAI MCP tools across different complexity levels and use cases.

---

## 1. EzyVet Login Workflow

**Complexity:** Beginner  
**Tests:** Basic `agent()`, `keyboard.type()`, validation, field clearing  
**Estimated Duration:** 30-60 seconds

### Example Prompts (Pick Any Style)

Users can request this workflow in various natural ways:

**Detailed & Structured:**
```
Create a workflow to login to EzyVet. Navigate to https://mybalto.usw2.trial.ezyvet.com/login.php, enter email mybalto.dev@trial.com and password @y7sxG$69cnMReJY, then verify we successfully logged in and reached the location selection page.
```

**Minimal & Direct:**
```
Login to https://mybalto.usw2.trial.ezyvet.com/login.php with mybalto.dev@trial.com / @y7sxG$69cnMReJY and confirm we're on the location page
```

**Conversational & Task-Oriented:**
```
I need a workflow that logs into my EzyVet trial account. The login page is https://mybalto.usw2.trial.ezyvet.com/login.php. Use email mybalto.dev@trial.com and password @y7sxG$69cnMReJY. Make sure it validates that we actually logged in successfully and are on the location selection screen.
```

**Step-by-Step Style:**
```
Build a workflow that:
1. Goes to the EzyVet login at https://mybalto.usw2.trial.ezyvet.com/login.php
2. Fills in mybalto.dev@trial.com for email
3. Fills in @y7sxG$69cnMReJY for password
4. Clicks login
5. Checks we're on the location selection page
```

**Casual & Brief:**
```
make a workflow to login to ezyvet. url is https://mybalto.usw2.trial.ezyvet.com/login.php, email mybalto.dev@trial.com, password @y7sxG$69cnMReJY. just validate we got to the location page after login
```

### Technical Specification

```
Create a workflow that automates login to the EzyVet trial portal.

The workflow should:
- Navigate to https://mybalto.usw2.trial.ezyvet.com/login.php
- Clear and fill in the email field with: mybalto.dev@trial.com
- Clear and fill in the password field with: @y7sxG$69cnMReJY
- Click the login/submit button
- Validate that we successfully logged in
- Check that we are now on the location selection page
- Return success=True if login was successful and location page is visible

Important:
- Always clear input fields before typing (ctrl+a, BackSpace)
- Check for error messages (invalid credentials, etc.)
- Validate we're on the location selection page, not still on login page

Input parameters:
- login_url: str (default: "https://mybalto.usw2.trial.ezyvet.com/login.php")
- email: str (default: "mybalto.dev@trial.com")
- password: str (default: "@y7sxG$69cnMReJY")

Output:
- success: bool
- current_page: str (description of the page we ended up on)
- error: str | None
```

---

## 2. Multi-Step Login with 2FA

**Complexity:** Intermediate  
**Tests:** Sequential validation, timing, error handling  
**Estimated Duration:** 60-90 seconds

### Prompt

```
Create a workflow that handles a two-factor authentication (2FA) login process.

The workflow should:
- Navigate to the login page at the specified URL
- Enter username and password credentials
- Click login button
- Wait for 2FA prompt to appear (timeout 20 seconds)
- Enter the provided 2FA code
- Click verify/submit button for 2FA
- Validate successful login by checking for dashboard or account page
- Check for error messages at each step
- Return appropriate success/failure status

Input parameters:
- login_url: str (default: "https://example.com/login")
- username: str
- password: str
- two_factor_code: str (6-digit code)

Output:
- success: bool
- current_page: str (description of where we ended up)
- error: str | None (specific error message if failed)
```

---

## 3. E-commerce Product Search & Price Extraction

**Complexity:** Intermediate  
**Tests:** `extract()` with structured data, navigation  
**Estimated Duration:** 45-75 seconds

### Prompt

```
Create a workflow that searches for a product and extracts pricing information.

The workflow should:
- Navigate to Amazon.com (or alternative e-commerce site)
- Use the search bar to search for the specified product
- Wait for search results to load
- Extract structured data from the first 5 search results including:
  - Product name
  - Price (as a number)
  - Rating (if available)
  - Number of reviews (if available)
  - Product URL
- Return the extracted data as a structured list

Input parameters:
- website_url: str (default: "https://www.amazon.com")
- search_query: str (e.g., "wireless mouse")
- max_results: int (default: 5)

Output:
- success: bool
- products: list[dict] (array of product objects)
- error: str | None

Product object schema:
{
  "name": str,
  "price": float,
  "rating": float | None,
  "review_count": int | None,
  "url": str
}
```

---

## 4. Calendar Event Creation

**Complexity:** Intermediate  
**Tests:** Date/time inputs, dropdown interactions  
**Estimated Duration:** 60-90 seconds

### Prompt

```
Create a workflow that creates a calendar event in Google Calendar.

The workflow should:
- Navigate to Google Calendar (https://calendar.google.com)
- Check if user is logged in, if not return error
- Click the "Create" or "+" button to create a new event
- Fill in the event details:
  - Event title
  - Date (handle date picker interaction)
  - Start time
  - End time
  - Description (optional)
  - Location (optional)
- Click Save/Create button
- Validate that the event appears on the calendar
- Return success status with event details

Input parameters:
- event_title: str (e.g., "Team Meeting")
- event_date: str (format: "YYYY-MM-DD")
- start_time: str (format: "HH:MM AM/PM")
- end_time: str (format: "HH:MM AM/PM")
- description: str | None
- location: str | None

Output:
- success: bool
- event_created: bool
- event_details: dict | None
- error: str | None
```

---

## 5. LinkedIn Profile Data Scraper

**Complexity:** Advanced  
**Tests:** Multi-page navigation, dynamic content, data aggregation  
**Estimated Duration:** 90-120 seconds

### Prompt

```
Create a workflow that extracts professional information from a LinkedIn profile.

The workflow should:
- Navigate to LinkedIn login page
- Log in with provided credentials
- Navigate to the specified LinkedIn profile URL
- Extract the following information:
  - Full name
  - Headline/title
  - Current company
  - Location
  - About/summary section
  - Work experience (last 3 positions with titles and companies)
  - Education (degree, school, years)
- Handle "Show more" buttons to expand truncated content
- Return structured profile data

Input parameters:
- linkedin_email: str
- linkedin_password: str
- profile_url: str (e.g., "https://www.linkedin.com/in/username")

Output:
- success: bool
- profile_data: dict (structured profile information)
- error: str | None

Profile data schema:
{
  "name": str,
  "headline": str,
  "current_company": str | None,
  "location": str,
  "about": str,
  "experience": [{"title": str, "company": str, "duration": str}],
  "education": [{"degree": str, "school": str, "years": str}]
}
```

---

## 6. File Upload & Download Validation

**Complexity:** Intermediate  
**Tests:** File handling, dialog interactions  
**Estimated Duration:** 60-90 seconds

### Prompt

```
Create a workflow that tests file upload and download functionality.

The workflow should:
- Navigate to a file sharing service (e.g., WeTransfer, Dropbox test page)
- Locate the file upload button/area
- Click to trigger upload (note: actual file dialog interaction may be limited)
- If possible, select and upload a test file
- Validate that upload progress is shown
- Wait for upload completion
- Verify the file appears in the uploaded files list
- Attempt to download the file back
- Validate download initiated

Input parameters:
- upload_url: str (default: file upload service URL)
- file_name: str (name of file to upload if accessible)

Output:
- success: bool
- upload_completed: bool
- download_initiated: bool
- file_verified: bool
- error: str | None

Note: This workflow may have limitations due to native file dialog restrictions.
```

---

## 7. Multi-Tab Research Workflow

**Complexity:** Advanced  
**Tests:** Tab management, context switching, data aggregation  
**Estimated Duration:** 120-180 seconds

### Prompt

```
Create a workflow that conducts research across multiple sources.

The workflow should:
- Open Google in a new tab and search for the specified topic
- Extract top 3 search result titles and snippets
- Open Wikipedia in a new tab and search for the same topic
- Extract the introduction paragraph
- Open a news site (e.g., CNN, BBC) in a new tab and search for the topic
- Extract recent news headline related to the topic
- Aggregate all findings into a structured research summary
- Return comprehensive data from all sources

Input parameters:
- research_topic: str (e.g., "artificial intelligence ethics")
- news_site: str (default: "https://www.bbc.com/news")

Output:
- success: bool
- research_data: dict
- error: str | None

Research data schema:
{
  "topic": str,
  "google_results": [{"title": str, "snippet": str}],
  "wikipedia_summary": str,
  "news_headline": str,
  "news_source": str
}
```

---

## 8. Form Auto-Fill with Validation Errors

**Complexity:** Advanced  
**Tests:** Error detection, retry logic, field validation  
**Estimated Duration:** 90-120 seconds

### Prompt

```
Create a workflow that intentionally triggers validation errors and recovers.

The workflow should:
- Navigate to a registration form with validation
- First attempt: Fill form with INVALID data (e.g., invalid email format, weak password)
- Click submit
- Detect and capture validation error messages
- Second attempt: Correct the errors field by field
- Clear and refill each field with VALID data
- Resubmit the form
- Validate successful submission
- Return a log of all validation issues encountered and how they were resolved

Input parameters:
- form_url: str (URL of form with validation)
- valid_email: str (e.g., "test@example.com")
- valid_password: str (e.g., "SecurePass123!")
- valid_name: str (e.g., "John Doe")

Output:
- success: bool
- validation_errors_encountered: list[str]
- errors_corrected: bool
- final_submission_status: str
- error: str | None
```

---

## 9. Social Media Cross-Posting

**Complexity:** Advanced  
**Tests:** Multiple platform interactions, authentication, media handling  
**Estimated Duration:** 120-180 seconds

### Prompt

```
Create a workflow that publishes the same content to multiple social media platforms.

The workflow should:
- Navigate to Twitter/X
- Log in with provided credentials
- Create a new post with the specified text content
- If image URL provided, attempt to attach the image
- Publish the post on Twitter/X
- Capture the post URL
- Navigate to LinkedIn
- Log in with LinkedIn credentials
- Create a new post with the same content
- Publish the post on LinkedIn
- Capture the LinkedIn post URL
- Validate both posts were published successfully
- Return URLs of both posts

Input parameters:
- twitter_username: str
- twitter_password: str
- linkedin_email: str
- linkedin_password: str
- post_content: str (the text to post)
- image_url: str | None (optional image to attach)

Output:
- success: bool
- twitter_post_url: str | None
- linkedin_post_url: str | None
- platforms_succeeded: list[str]
- platforms_failed: list[str]
- error: str | None
```

---

## 10. Comparison Shopping Workflow

**Complexity:** Expert  
**Tests:** Complex navigation, data extraction, comparison logic  
**Estimated Duration:** 150-240 seconds

### Prompt

```
Create a workflow that compares product prices across multiple retailers.

The workflow should:
- Navigate to Amazon.com
- Search for the specified product
- Extract the first result's:
  - Product name
  - Price
  - Availability status
  - Product URL
- Navigate to Walmart.com
- Search for the same product
- Extract similar details from Walmart
- Navigate to Target.com
- Search for the same product
- Extract similar details from Target
- Compare all three prices
- Determine which retailer has the best deal
- Return comprehensive comparison data

Input parameters:
- product_name: str (e.g., "Sony WH-1000XM5 Headphones")
- amazon_url: str (default: "https://www.amazon.com")
- walmart_url: str (default: "https://www.walmart.com")
- target_url: str (default: "https://www.target.com")

Output:
- success: bool
- comparison_data: dict
- best_deal: dict
- error: str | None

Comparison data schema:
{
  "product_searched": str,
  "retailers": [
    {
      "name": str,
      "product_name": str,
      "price": float,
      "available": bool,
      "url": str
    }
  ],
  "best_deal": {
    "retailer": str,
    "price": float,
    "savings": float (compared to highest price)
  }
}
```

---

## Testing Strategy

### Recommended Testing Order

1. **Workflow #1** → Establish baseline functionality
2. **Workflow #2** → Test sequential validation and timing
3. **Workflow #3** → Validate data extraction capabilities
4. **Workflow #8** → Test error recovery mechanisms
5. **Workflow #4** → Test UI element interactions
6. **Workflow #6** → Test file handling (with limitations)
7. **Workflow #5** → Test complex data scraping
8. **Workflow #7** → Test multi-tab management
9. **Workflow #9** → Test multi-platform workflows
10. **Workflow #10** → Stress test with full complexity

### Success Metrics to Track

- **Execution Time**: How long each workflow takes
- **Success Rate**: Percentage of successful runs
- **Error Types**: What kinds of errors occur most frequently
- **Reliability**: Consistency across multiple runs
- **Platform Limitations**: What doesn't work as expected

### How to Use These Prompts

Simply copy the prompt text under each workflow and provide it to the AI assistant, prefaced with:

```
Create a workflow that [paste prompt here]
```

The AI will follow the workflow creation process defined in the `.cursor/rules` to build, validate, deploy, and test each workflow.

---

## Notes

- **Authentication**: Some workflows require real credentials. Use test accounts.
- **Rate Limiting**: Be mindful of API/website rate limits when testing
- **Dynamic Content**: Websites change; workflows may need adjustments
- **Browser State**: Some workflows assume clean browser state (no cookies)
- **File System**: File upload/download may have platform limitations

## Iteration Tips

After running each workflow:
1. Review the logs to understand VLM decision-making
2. Note any unexpected behavior or failures
3. Iterate on validation logic if false positives/negatives occur
4. Adjust timeouts if operations are too slow
5. Document platform-specific quirks discovered

---

**Last Updated:** February 9, 2026  
**Version:** 1.0
