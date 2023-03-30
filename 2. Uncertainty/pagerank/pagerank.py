import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    """print(corpus)
    print(corpus.keys())
    print(list(corpus.keys()))
    for key in corpus.keys():
        print(key)
    print(corpus.values())"""
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #print(corpus)
    total_links = len(corpus[page])
    total_pages = len(corpus)

    pagerank = corpus.copy()

    if total_links > 0:

        #   Gets the amount of links to each page from the current page
        link_count = dict()
        for html_page in corpus[page]:
            if html_page in link_count:
                link_count[html_page] = link_count[html_page] + 1
            else:
                link_count[html_page] = 1

        #   Asigns proper values to each page
        for html_page in corpus:
            pagerank[html_page] = (1 - damping_factor) / total_pages
            if html_page in link_count:
                pagerank[html_page] = pagerank[html_page] + (damping_factor / total_links * link_count[html_page])

    else:
        #   If no links to other pages, then all values will be equal
        equal_values = 1 / len(corpus)
        for page in corpus:
            pagerank[page] = equal_values

    return pagerank


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pagerank = dict()

    next_page = random.choice(list(corpus))
    for i in range(n - 1):
        model = transition_model(corpus, next_page, damping_factor)

        model_keys = list(model.keys())
        model_values = list(model.values())

        next_page = random.choices(model_keys, model_values)[0]

        if next_page in pagerank:
            pagerank[next_page] += 1
        else:
            pagerank[next_page] = 1
            
    for page in pagerank:
        pagerank[page] = pagerank[page] / n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    total_pages = len(corpus)
    pagerank = dict()

    for page in corpus:
        pagerank[page] = 1 / total_pages

    to_break = False
    while not to_break:
        pr_copy = pagerank.copy()

        for page in pagerank:
            sum = 0
            for linked_page in pagerank:
                if page in corpus[linked_page]:
                    sum += pagerank[linked_page] / len(corpus[linked_page])
                elif len(corpus[linked_page]) == 0:
                    sum += 1 / total_pages

            pagerank[page] = (1 - damping_factor) / total_pages + damping_factor * sum

        pr_diff = dict()
        for page in pagerank:
            pr_diff[page] = abs(pagerank[page] - pr_copy[page])

        to_break = True
        for page in pr_diff:
            if pr_diff[page] > 0.001:
                to_break = False

    return pagerank


if __name__ == "__main__":
    main()
