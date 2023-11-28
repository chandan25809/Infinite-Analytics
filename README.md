## Prerequisites
- watch this demo [video](https://drive.google.com/file/d/16_gkWhLlDfck-9_b7k6FAGYi5CY4EwMu/view?usp=sharing)
- Python 3.x
- [Virtualenv](https://virtualenv.pypa.io/en/latest/)

## Obtaining Google OAuth Credentials

To use Google OAuth for authentication, you'll need to obtain credentials. Follow these steps:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. In the left sidebar, navigate to "APIs & Services" > "Credentials."
4. Click on "Create Credentials" and select "OAuth client ID."
5. Configure the consent screen and application type.
6. Add the authorized redirect URI (e.g., `http://localhost:8000/auth_app/auth`).
7. After creating the OAuth client ID, copy the generated client ID and client secret.
8. Update the `.env.test` file in the root of your project with the obtained credentials.

Make sure to replace `YOUR_TEST_CLIENT_ID` and `YOUR_TEST_CLIENT_SECRET` in the `.env.test` file with the actual values you obtained.

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/chandan25809/Infinite-Analytics.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Infinite-Analytics
    ```

3. Create a virtual environment:

    ```bash
    virtualenv venv
    ```

4. Activate the virtual environment:

    On Windows:

    ```bash
    .\venv\Scripts\activate
    ```

    On macOS/Linux:

    ```bash
    source venv/bin/activate
    ```

5. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
## Running the Application

1. Run the application:

    ```bash
    uvicorn main:app --reload
    ```
2. Open your web browser and go to [http://localhost:8000](http://localhost:8000).

3. You should see your application running. Follow the provided URLs in the terminal for specific routes.

## Deactivating the Virtual Environment

When you're done working on your project, deactivate the virtual environment:

```bash
deactivate
