#Script that gets all files in the folder pages and keeps only the visible text
#Saving the result in the folder pages_preprocessed
from bs4 import BeautifulSoup
from bs4.element import Comment
import os

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body.read(), 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def preprocess_site_pages(folder, site, label):
    if(label not in ["bad", "good"]):
        raise NameError("The possible labels are good or bad")

    actual_folder_path = os.path.abspath(folder + "/" + site + "/" + label)
    processed_pages_folder = "pages_preprocessed/" + label + "/"

    for file in os.listdir(actual_folder_path):
        if(file.endswith(".html")):
            file_path = os.path.abspath(actual_folder_path + "/" + file)
            html = open(file_path)
            #Preprocess HTML page
            html_visible_text = text_from_html(html)
            #Save to file for later use
            new_file_name = processed_pages_folder + file[:5] + ".txt"
            count = 0
            while(os.path.isfile(new_file_name)):
                count += 1
                new_file_name = processed_pages_folder + file[:5] + str(count) + ".txt"
            thefile = open(new_file_name, 'w')
            thefile.write("%s\n" % html_visible_text.encode('utf8'))
        else:
            raise NameError("Files in folder must be hmtl files")

def main():
    folder_path = os.path.abspath("pages")
    #Get all the site folders labeled in pages
    site_folders = os.listdir(folder_path)

    # try:
    os.makedirs(os.path.abspath("pages_preprocessed/good"))
    os.makedirs(os.path.abspath("pages_preprocessed/bad"))

    for site in site_folders:
        preprocess_site_pages("pages", site, "bad")
        preprocess_site_pages("pages", site, "good")
    # except:
    #     print("Remove existing folder to continue!")



if __name__ == "__main__":
    main()
