import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
import time
import os
import random
from multiprocessing import Pool, cpu_count # Import Pool and cpu_count for parallel processing

# --- Creator Information and Disclaimer ---
CREATOR_INFO = """
----------------------------------------------------
Developed with passion by Sheikh Bilal
A Java developer who loves coding and automation.

Connect with me:
GitHub: https://github.com/sheikh-bilal65
LinkedIn: https://www.linkedin.com/in/bilal-ahmad2
Gmail: bilalahmadallbd@gmail.com

Support my work:
Buy Me a Coffee: https://buymeacoffee.com/bilalsheikh
Crypto Donation (Binance ID): 150697028
Your support motivates me to upload more free and feature-rich tools!
----------------------------------------------------
DISCLAIMER:
This tool is provided for educational purposes only.
It demonstrates automation techniques and is not intended for violating
Instagram's Terms of Service or any applicable laws.
The creator, Sheikh Bilal, is not responsible for any misuse of this tool
or any consequences that may arise from its use.
Users are solely responsible for adhering to Instagram's policies and local regulations.
----------------------------------------------------
"""

def setup_driver(username=None):
    """Sets up the Chrome WebDriver with optional user data directory for session persistence."""
    chrome_options = Options()
    # Optional: Add headless mode if you don't want to see the browser UI
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu") # Added to prevent potential GPU-related issues
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # For session persistence: use a unique user data directory for each account
    if username:
        user_data_dir = os.path.join(os.getcwd(), "chrome_profiles", username)
        os.makedirs(user_data_dir, exist_ok=True)
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        print(f"Using Chrome profile: {user_data_dir}")

    # Add a small random delay before launching the driver to mitigate race conditions
    time.sleep(random.uniform(0.5, 1.5)) 
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(900, 600) # Set window size for consistency
    return driver

def dismiss_popups(driver):
    """Attempts to dismiss common Instagram pop-ups."""
    print("Attempting to dismiss pop-ups...")
    # Cookie consent banner (EU/first visit)
    try:
        cookie_btn = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((By.XPATH,
                "//button[normalize-space(.)='Allow all cookies' or normalize-space(.)='Allow all' or normalize-space(.)='Only allow essential cookies' or contains(., 'Allow essential') or contains(., 'Accept all')]"
            ))
        )
        cookie_btn.click()
        print("Dismissed cookie consent banner.")
        time.sleep(random.uniform(0.5, 1)) # Reduced sleep
    except:
        pass
    # "Add Instagram to your home screen" pop-up (common on mobile view)
    try:
        cancel_button_add_to_home = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Cancel']"))
        )
        cancel_button_add_to_home.click()
        print("Dismissed 'Add Instagram to your home screen' prompt.")
        time.sleep(random.uniform(0.5, 1)) # Reduced sleep
    except:
        pass

    # "Turn on Notifications" prompt
    try:
        not_now_button_notifications = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))
        )
        not_now_button_notifications.click()
        print("Dismissed 'Turn on Notifications' prompt.")
        time.sleep(random.uniform(0.5, 1)) # Reduced sleep
    except:
        pass

    # Any other generic "Not Now" or "Close" buttons that might appear
    try:
        generic = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(.)='Not Now' or normalize-space(.)='Close' or @aria-label='Close' or @aria-label='Dismiss'] | //div[@role='button' and (normalize-space(.)='Not Now' or @aria-label='Close')] | //div[@role='dialog']//button[@type='button']"))
        )
        generic.click()
        print("Dismissed a generic 'Not Now' or 'Close' pop-up.")
        time.sleep(random.uniform(0.5, 1)) # Reduced sleep
    except:
        pass

def read_accounts(file_path):
    """Reads accounts from an Excel file."""
    try:
        df = pd.read_excel(file_path)
        # Ensure 'username' and 'password' columns exist
        if 'username' not in df.columns or 'password' not in df.columns:
            raise ValueError("Excel file must contain 'username' and 'password' columns.")
        return df.to_dict(orient='records')
    except FileNotFoundError:
        print(f"Error: Account file not found at {file_path}")
        return []
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return []

def login_instagram(driver, username, password):
    """Logs into Instagram, handling session persistence and common pop-ups."""
    print(f"Attempting to log in with username: {username}")
    
    # First, check if already logged in by navigating to the home page and looking for a key element
    driver.get("https://www.instagram.com/")
    # Reduced initial sleep, relying more on explicit waits
    try:
        # Look for the absence of the username input field to confirm login
        WebDriverWait(driver, 10).until( # Reduced wait time
            EC.invisibility_of_element_located((By.NAME, "username"))
        )
        print(f"Already logged in as {username} (session found).")
        # Dismiss any pop-ups that might appear on the home feed after a fresh session load
        dismiss_popups(driver)
        return True
    except TimeoutException: # Catch specific TimeoutException if not logged in
        print(f"Not logged in as {username} or session expired. Proceeding with explicit login.")
        # If not logged in, explicitly go to the login page
        driver.get("https://www.instagram.com/accounts/login/")
        # Reduced initial sleep, relying more on explicit waits
        try:
            # Wait for username field to be present
            username_field = WebDriverWait(driver, 15).until( # Reduced wait time
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = driver.find_element(By.NAME, "password")
            
            username_field.send_keys(username)
            password_field.send_keys(password)
            
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            login_button.click()
            
            # Reduced delay after clicking login, relying more on explicit waits
            WebDriverWait(driver, 20).until( # Reduced wait time
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")), # Search bar on home feed
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/accounts/edit/')]")), # Profile link
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x1iyjqo2')]")), # A common div class on the home feed
                    EC.presence_of_element_located((By.XPATH, "//span[text()='Home']")) # Home icon text
                )
            )
            print(f"Successfully logged in as {username}")

            # Handle "Save Your Login Info?" prompt (this is specific, so keep it separate)
            try:
                not_now_button_save_info = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))
                )
                not_now_button_save_info.click()
                print("Clicked 'Not Now' on 'Save Your Login Info?' prompt.")
                time.sleep(random.uniform(0.5, 1)) # Reduced sleep
            except:
                pass
            
            # Dismiss any other general pop-ups that might appear after login
            dismiss_popups(driver)

            return True
        except Exception as e:
            # If successful login elements are not found, check for common error messages
            try:
                error_message_element = WebDriverWait(driver, 5).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Sorry, your password was incorrect')]")),
                        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'The username you entered doesn\'t belong to an account.')]")),
                        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Please check your username and try again.')]")),
                        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'There was a problem logging you in.')]"))
                    )
                )
                print(f"Login failed for {username}. Error message: {error_message_element.text}")
            except:
                print(f"Login failed for {username}. No specific error message found, or page structure changed. Error: {e}")
            return False
            
    except Exception as e: # This catch-all is for any other unexpected errors during the initial login check or subsequent explicit login
        print(f"An unexpected error occurred during login for {username}: {e}")
        return False

def perform_task(driver, task_url, task_type="visit", comment_text="Great post!", watch_time=45):
    """Performs a specified task on Instagram."""
    print(f"Performing task: {task_type} on {task_url}")
    driver.get(task_url)
    
    is_reel = "/reel/" in task_url.lower()
    try:
        try:
            WebDriverWait(driver, 10).until(EC.url_contains(task_url.split('?')[0]))
        except Exception as e:
            print(f"Warning: URL check failed after navigation: {e}")
        print(f"Navigated to {task_url}")

        dismiss_popups(driver)

        if task_type == "visit":
            print(f"Visited URL: {task_url}")
        elif task_type == "like":
            print(f"Attempting to like post at: {task_url}")
            
            dismiss_popups(driver)

            try:
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//*[name()='svg' and @aria-label='Unlike']"))
                )
                print("Post is already liked. Skipping.")
                time.sleep(random.uniform(0.2, 0.5))
                return "already_liked"
            except TimeoutException:
                print("Post is not yet liked, proceeding to find like button.")
                pass

            try:
                like_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[name()='svg' and @aria-label='Like']/ancestor::button | //*[name()='svg' and @aria-label='Like']/ancestor::div[@role='button']"))
                )
                like_button.click()
                print("Successfully clicked the 'Like' button.")
                time.sleep(random.uniform(0.7, 2))

                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//*[name()='svg' and @aria-label='Unlike']"))
                    )
                    print("Successfully verified the post was liked (Unlike button found).")
                    return "liked_successfully"
                except TimeoutException:
                    print("Could not verify like (Unlike button not found after action).")
                    return "like_failed_verification"

            except TimeoutException:
                print("Like button not found or not clickable within the timeout.")
                return "like_button_not_found"
            except Exception as e:
                print(f"An error occurred while trying to like the post: {e}")
                return "like_error"
            
            time.sleep(random.uniform(0.2, 0.5))
        elif task_type == "comment":
            print(f"Attempting to comment on post at: {task_url}")
            comment_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Add a comment…']"))
            )
            comment_input.click()
            time.sleep(random.uniform(0.2, 0.5))
            comment_input.send_keys(comment_text)
            
            post_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Post']"))
            )
            post_button.click()
            print(f"Commented: '{comment_text}' on the post.")
            time.sleep(random.uniform(0.5, 1.5))
            return "commented_successfully"
        elif task_type == "reel_view":
            print(f"Attempting to view reel at: {task_url}")
            # Apply watch time constraints
            actual_watch_duration = max(0, min(watch_time, 120)) # Ensure between 0 and 120
            if actual_watch_duration == 0: # If input was <= 0, default to 45
                actual_watch_duration = 45
            
            print(f"Simulating reel view for {actual_watch_duration:.1f} seconds.")
            time.sleep(actual_watch_duration)
            print(f"Viewed reel at: {task_url} for {actual_watch_duration:.1f} seconds.")
            return {"status": "viewed_reel", "duration": actual_watch_duration}
        elif task_type == "story_view":
            print(f"Attempting to view story at: {task_url}")
            view_duration = random.uniform(3, 8)
            print(f"Simulating story view for {view_duration:.1f} seconds.")
            time.sleep(view_duration)
            print(f"Viewed story at: {task_url}")
            return {"status": "viewed_story", "duration": view_duration}
        else:
            print(f"Unknown task type: {task_type}")
            return {"status": "unknown_task_type", "duration": 0}
            
    except Exception as e:
        print(f"An error occurred during task '{task_type}' on {task_url}: {e}")
        screenshot_name = f"error_{task_type}_{time.strftime('%Y%m%d-%H%M%S')}.png"
        driver.save_screenshot(screenshot_name)
        print(f"Screenshot saved as {screenshot_name}")
        return {"status": "task_error", "duration": 0}

import argparse

def main():
    parser = argparse.ArgumentParser(description="Instagram Automation Script")
    parser.add_argument("--url", required=True, help="Target Instagram URL (post, reel, or user profile)")
    parser.add_argument("--likes", type=int, default=0, help="Number of likes to perform")
    parser.add_argument("--comments", type=int, default=0, help="Number of comments to perform")
    parser.add_argument("--shares", type=int, default=0, help="Number of shares to perform (not yet implemented)")
    parser.add_argument("--reel-views", type=int, default=0, help="Number of reel views to perform")
    parser.add_argument("--story-views", type=int, default=0, help="Number of story views to perform")
    parser.add_argument("--reel-watch-time", type=int, default=45, 
                        help="Duration in seconds to watch each reel. Must be between 0 and 120. "
                             "If less than 0, defaults to 45. If greater than 120, defaults to 120.")
    
    args = parser.parse_args()

    accounts_file = "account.xlsx"
    accounts = read_accounts(accounts_file)
    
    if not accounts:
        print("No accounts found or could not read accounts file. Exiting.")
        return

    num_available_accounts = len(accounts)
    print(f"Found {num_available_accounts} accounts in {accounts_file}.")

    final_tasks_to_execute = []
    
    for i in range(min(args.likes, num_available_accounts)):
        final_tasks_to_execute.append((accounts[i], args.url, "like", "Great post!", args.reel_watch_time))
    if args.likes > num_available_accounts:
        print(f"Warning: Requested {args.likes} likes but only {num_available_accounts} unique accounts are available for liking. Attempting {min(args.likes, num_available_accounts)} likes.")

    for i in range(min(args.comments, num_available_accounts)):
        final_tasks_to_execute.append((accounts[i], args.url, "comment", "Great post!", args.reel_watch_time))
    if args.comments > num_available_accounts:
        print(f"Warning: Requested {args.comments} comments but only {num_available_accounts} unique accounts are available for commenting. Attempting {min(args.comments, num_available_accounts)} comments.")

    for i in range(min(args.reel_views, num_available_accounts)):
        final_tasks_to_execute.append((accounts[i], args.url, "reel_view", "Great post!", args.reel_watch_time))
    if args.reel_views > num_available_accounts:
        print(f"Warning: Requested {args.reel_views} reel views but only {num_available_accounts} unique accounts are available for viewing reels. Attempting {min(args.reel_views, num_available_accounts)} reel views.")

    for i in range(min(args.story_views, num_available_accounts)):
        final_tasks_to_execute.append((accounts[i], args.url, "story_view", "Great post!", args.reel_watch_time))
    if args.story_views > num_available_accounts:
        print(f"Warning: Requested {args.story_views} story views but only {num_available_accounts} unique accounts are available for viewing stories. Attempting {min(args.story_views, num_available_accounts)} story views.")

    if not final_tasks_to_execute:
        print("No tasks requested or no accounts available for tasks. Exiting.")
        return

    print(f"Prepared {len(final_tasks_to_execute)} total unique tasks to be executed.")
    
    num_processes = min(2, cpu_count(), len(final_tasks_to_execute))
    print(f"Using {num_processes} processes for automation.")

    results = []
    with Pool(processes=num_processes) as pool:
        results = pool.starmap(process_account_task, final_tasks_to_execute)
            
    print("\n--- Automation Summary ---")
    print(f"Requested {args.likes} likes, {args.comments} comments, {args.reel_views} reel views, {args.story_views} story views.")
    print(f"Found {num_available_accounts} accounts in {accounts_file}.")

    total_likes_attempted = 0
    total_likes_successful = 0
    total_already_liked = 0
    total_comments_successful = 0
    total_reel_views_successful = 0
    total_story_views_successful = 0
    total_reel_watch_time_seconds = 0
    
    for result in results:
        if isinstance(result, dict):
            status = result.get("status")
            duration = result.get("duration", 0)
        else: # Handle old string results for compatibility
            status = result
            duration = 0

        if status == "liked_successfully":
            total_likes_successful += 1
            total_likes_attempted += 1
        elif status == "already_liked":
            total_already_liked += 1
            total_likes_attempted += 1
        elif status == "commented_successfully":
            total_comments_successful += 1
        elif status == "viewed_reel":
            total_reel_views_successful += 1
            total_reel_watch_time_seconds += duration
        elif status == "viewed_story":
            total_story_views_successful += 1

    print(f"\nTotal likes attempted: {total_likes_attempted}")
    print(f"  - New likes given: {total_likes_successful}")
    print(f"  - Posts already liked: {total_already_liked}")
    print(f"Total comments given: {total_comments_successful}")
    print(f"Total reel views performed: {total_reel_views_successful}")
    print(f"Total story views performed: {total_story_views_successful}")

    # Calculate total reel watch time in minutes and seconds
    total_minutes = int(total_reel_watch_time_seconds // 60)
    remaining_seconds = int(total_reel_watch_time_seconds % 60)
    print(f"Total reel watch time: {total_minutes} minutes and {remaining_seconds} seconds.")

    print("\nAutomation complete.")

def process_account_task(account, url, task_type, comment_text, watch_time):
    """Function to be run by each process for a single account and task."""
    username = account['username']
    password = account['password']
    
    print(f"\n[Process for {username}] Starting task: {task_type} on {url}")
    
    driver = setup_driver(username)

    task_result = {"status": "failed", "duration": 0} # Initialize with a dictionary
    try:
        if login_instagram(driver, username, password):
            task_result = perform_task(driver, url, task_type, comment_text, watch_time)
        else:
            print(f"[Process for {username}] Skipping task due to login failure.")
            task_result["status"] = "login_failed"
    except Exception as e:
        print(f"[Process for {username}] An error occurred during automation: {e}")
        task_result["status"] = "process_error"
    finally:
        driver.quit()
    return task_result

if __name__ == "__main__":
    print(CREATOR_INFO)
    
    from multiprocessing import freeze_support
    freeze_support()
    main()
