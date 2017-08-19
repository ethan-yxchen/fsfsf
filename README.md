# FSFSF - _Fast_ _Search_ _for_ _Similar_ _Files_ in large collection of files

FSFSF searches for similar files and similar parts of files in a large-scale collection of files.

Mining for [resemblance and containment of documents(Broder 1997)](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.24.779&rep=rep1&type=pdf) has long been important since the days of AltaVista, even before Google was born; search engine giants are doing really well nowaday, but there is not a simple, succinct open source project to address this problem and provide a general purpose module.

When we talk about similarity of two files, we are talking about that the two sets of features of these two files has a large intersection. For example, depending on application, you may find that you consider two files similar as long as their bags of 2-grams are 80% intersected. This similarity is formally defined by [Jaccard Distance](https://en.wikipedia.org/wiki/Jaccard_index).

And more than often, we may notice that just one part of a file is very similar to some other file, or a portion of the other file. A paragraph in an article can be similar to another paragraph in some other article, even if the articles are just 30% similar. Or a code block can be a near-clone to another code block in some other source file -- then you know maybe it's time for refactoring. Or when you identify a malicious attachment (payload) of a intentionally malformated PDF file, that payload might be found resemble to a payload in another cyberattack.

FSFSF solves these problems and empowers you to discvoer similarity relations within a large collections of files. You can do the following:

- Given a collection of files, reporting approximately all pairs of similar files,
- Or more efficiently, reporting clusters of similar files,
- Or, for a single file, seen or unseen before, find almost every file similar to it. This is lightning fast, like Google's search image by image.

What's more, you can query for parts of files, **without laborious effort to define and implement parsing of files into parts**. It is an important advantage for unstructured files that you don't know how to parse, for semi-structured file, and for embedded contents (for example, suspicious string in javascript which can later be evaluated and reflected into code).

FSFSF is built on two ideas: Disjunction of Conjunction of Minhash (DC-Minhash) and File Fragment Clone Search (FFCS).

DC-Minhash provides a scalable, sort-and-groupby style clustering or pre-clustering algorithm. Sort-and-groupby approach is O(n log n) to the size of collection, and this is better then many clustering algorithms which requires all-pair distance, of O(n log n).

The vanila version of MinHash is a locality sensitiity hashing that use hamming distance among fix-size MinHash of as an estimater of Jaccard distance among sets. You still need to compute the distances when use. The first work which use the sort-and-groupby approach on MinHash is described in Cohen et al. (2001).

And if you look at the fuzzy digests widely adapt in practice, such as Nilsimsa hash, ssdeep, you also need to compute the distances. With appropirate overhead, DC-minhash can be a better choice when scale is really an issue.
