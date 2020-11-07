/* Spam blob */
const spam = ['readme', 'readme.md', 'modified readme.md', 'change', 'update', 'contributing', 'contributing.md', 'create', 'modify', 'modify readme','basic blogging','create readmekorean','patch', 'user', 'file', 'add','change contributing', 'modified contributing','html templates','.md','md']

/* Check count of a substring in the string */
const counter = (main_str, sub_str) =>
    {
    main_str += '';
    sub_str += '';

    if (sub_str.length <= 0) 
    {
        return main_str.length + 1;
    }

       subStr = sub_str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
       return (main_str.match(new RegExp(subStr, 'gi')) || []).length;
    }

/* Count the total spam keywords in the PR */
const spam_count =(text_corpus)=>{
    const count = 0 ;
    for (word in spam){
        count = count + counter(text_corpus,word)
    }
    return count
}