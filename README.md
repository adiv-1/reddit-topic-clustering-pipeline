# Reddit Forum Scraper, Clustering & Real-Time Analysis System 

### Project Overview
This project implements an end-to-end Reddit data pipeline that performs:
* Web scraping of Reddit posts
* Data preprocessing and cleaning
* OCR-based text extraction from images
* Structured storage in MySQL
* Transformer-based document embeddings
* K-Means clustering of posts
* PCA-based visualization
* Real-time automated data updates
* Interactive semantic cluster querying

The system was developed using Python 3.11 on Ubuntu Linux, with all components executed through an SSH-connected VS Code environment.

This project demonstrates practical experience with:
* Web scraping strategies
* Data engineering
* NLP embeddings
* Clustering algorithms
* Database integration
* Automation pipelines
* Real-time data processing

### Environment Setup 
**Operating System**

* Ubuntu Linux (VM)
* NAT Network Adapter with Port Forwarding
* SSH connection to host via VS Code

**Database**

* MySQL Server (installed on Ubuntu)
* Database: `reddit_db`
* Dedicated application user with full privileges

**Python Version**
* Python 3.11

**Python Libraries**
```
requests
beautifulsoup4
mysql-connector-python
sentence-transformers
scikit-learn
pytesseract
Pillow
matplotlib
```
**Source Files**

* `main.py`: Automation and interactive interface
* `scraper.py`: Reddit scraping logic
* `preprocessing.py`: Text cleaning and normalization
* `ocr.py`: Image OCR extraction
* `db.py`: MySQL database operations
* `embedding_cluster.py`: Embedding generation and clustering
* `visualization.py`: PCA visualization

### Data Collection 
**Target Subreddits**
* r/careerguidance
* r/jobs
* r/cscareerquestions
* r/resume
* r/career

**Scraping Methods Tested**

We evaluated multiple scraping approaches:

* Reddit `.json` endpoints --> Fast but limited to ~1000 posts, rate limited
* Selenium (Headless Chrome) --> CAPTCHA issues, unstable DOM selectors
* BeautifulSoup (old.reddit.com) --> Selected method

**Why BeautifulSoup + old.reddit.com?**
* Static HTML (no JS rendering issues)
* No CAPTCHA interruptions
* Stable DOM structure
* Efficient parsing
* Avoids heavy browser automation overhead

**Handling Large Requests**
* Supports 1000+ post requests
* Uses pagination with `after` parameter
* Controlled request delays
* Handles API limits safely
* Uses `INSERT IGNORE` to prevent duplicates

### Data Preprocessing 
Implemented in `preprocessing.py` and `ocr.py`.

**Cleaning Steps**
* Remove HTML tags
* Remove URLs
* Remove special characters
* Normalize to lowercase
* Remove extra whitespace
* Filter promoted posts
* Convert timestamps to UTC
* Mask usernames using salted SHA-256 hashing

**OCR Processing**
* Some posts include images. We:
* Validate image type & size
* Extract text using pytesseract
* Clean OCR output
* Merge OCR text with title + body

### Embeddings and Clustering 
Implemented in `embedding_cluster.py`.

**Embedding Model**

We used:
```
sentence-transformers
Model: all-MiniLM-L6-v2
Output dimension: 384
```

**Why Not Doc2Vec?**

Although Doc2Vec was considered:
* Transformer-based embeddings provide stronger semantic representation
* Better contextual understanding
* Improved clustering quality during testing

Embeddings are:
* Normalized
* Stored in MySQL as JSON
* Reused for clustering and querying

### Clustering

Algorithm: K-Means (Scikit-Learn)

Number of clusters: K = 5

For each cluster:
* Identify document closest to centroid
* Extract cluster keywords using TF-IDF
* Store cluster ID in database

**Visualization**

Implemented in `visualization.py`:
* PCA reduces 384D embeddings → 2D
* Each point represents a Reddit post
* Color-coded by cluster ID

### Automation and Real-Time Processing 
The entire pipleine is automated through `main.py`.

**Usage**
```
python main.py <interval_seconds> <posts_per_subreddit>
```

**Example**
```
python main.py 300 500
```

This means:
* Update every 300 seconds (5 minutes)
* Fetch 500 posts per subreddit per cycle

**Pipeline Flow**
1. Scrape posts
2. Preprocess text
3. Run OCR (if images exist)
4. Generate embeddings
5. Perform clustering
6. Update database
7. Sleep until next cycle


### Key Features
* Multiple scraping strategies evaluated
* Robust rate-limit handling
* Large-request support (5000+ posts)
* OCR integration
* Privacy-preserving username masking
* Transformer-based semantic embeddings
* Automated clustering
* PCA visualization
* Real-time update loop
* Interactive semantic cluster querying
