from libcpp.vector cimport vector

# cdef extern from "test.h":
#     cdef int analyze2(
#         const char* document,
#         int length)
#

cdef extern from "document.cpp":
    cdef cppclass Document:
        Document(char *doc, int size)
        void Tokenize()
        void ArgsortTokens()
        void MakeTwoGrams()
        void ShowTwoGrams()
        void ShowUnique()
        void ShowRenamedTokens()
        int num_tokens()
        int num_unique()
        int num_twograms()

cpdef test(char *document, int length):
    #analyze2(document, length)
    doc = new Document(document, length)
    doc.Tokenize()
    doc.ArgsortTokens()
    #doc.ShowUnique()
    # doc.ShowRenamedTokens()
    doc.MakeTwoGrams()
    a = doc.num_unique()
    b = doc.num_twograms()
    c = doc.num_tokens()
    #doc.ShowTwoGrams()
    del doc
    return a, b, c


# def tokenize(char* document, int length):
#     cdef vector[int] *ends = new vector[int]()
#     cdef vector[char] *buf = new vector[char]()
#     cdef vector[int] *counts = new vector[int]()
#     cdef char *d
#     cdef bytes s
#     try:
#         analyze(document, length, ends, buf, counts)
#         start = 0
#         d = <char*>(counts[0].data())
#         print d[:8]
#         #for end in ends[0][:5]:
#         #    s = d[start:end]
#         #    print s,
#         #    start = end
#         print
#     finally:
#         del ends
#         del buf
#         del counts
