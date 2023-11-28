## Prerequisites

- Python 3.x
- [Virtualenv](https://virtualenv.pypa.io/en/latest/)

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
