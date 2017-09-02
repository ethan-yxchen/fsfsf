#include <array>
#include <string>
#include <vector>

#include <algorithm>

#include <cassert>
#include <cstdio>

//#include <x86intrin.h>

bool IsTargetChar(char c);

using namespace std;

struct Token {
  int pos;
  int len;
  Token() {}
  Token(int pos, int len) : pos(pos), len(len) {}
};

/**
TokEq: functor with state

Test if tokens x and y are equal with respect to document_
*/
class TokEq {
 public:
  TokEq(const char *doc) : document_(doc) {}

  bool operator()(const Token &x, const Token &y) const {
    if (x.len != y.len) { return false; }
    if (x.pos == y.pos) { return true; }
    const char *sx = document_ + x.pos;
    const char *sy = document_ + y.pos;
    for (int i=0, end=x.len; i < end; ++i)
      if (sx[i] != sy[i])
        return false;
    return true;
    }
 private:
  const char* document_;
};

/**
TokCmp: functor with state

Test if tokens x < y with respect to document_
*/
class TokCmp {
 public:
  TokCmp(const char *doc) : document_(doc) {}

  bool operator()(const Token &x, const Token &y) const {
    if (x.pos == y.pos) { return x.len < y.len; }
    const char *sx = document_ + x.pos;
    const char *sy = document_ + y.pos;
    int nx = x.len, ny = y.len;
    int nz = (nx < ny)? nx : ny;
    for (int i=0; i < nz; ++i) {
      if (sx[i] < sy[i]) { return true; }
      if (sx[i] > sy[i]) { return false; }
    }
    return nx < ny;
  }
 private:
  const char* document_;
};

/**
TokPrint: functor with state

Print token
*/
class TokPrint {
 public:
  TokPrint(const char *doc) : document_(doc) {}

  void operator()(const Token &t) const {
    const char *s = document_ + t.pos;
    for (int i = 0; i < t.len; ++i)
      printf("%c", s[i]);
  }
 private:
  const char* document_;
};

template <class Iterator, class EQ, class ForEach>
void groupby(Iterator begin, Iterator end, EQ eq, ForEach foreach) {
  if (begin == end) { return; }
  auto a = begin, b = begin + 1;
  for (; b < end; ++b)
    if (!eq(*a, *b))
      foreach(a, b), a = b;
  foreach(a, b);
}

class Document {
 public:
  Document(const char *doc, int size)
      : tok_eq(doc), tok_comp(doc), tok_print(doc),
        document_(doc), size_(size) {}

  TokEq tok_eq;
  TokCmp tok_comp;
  TokPrint tok_print;

  const int *md5() const { return md5_; }
  int size() const { return size_; }
  const Token *tokens() const { return tokens_.data(); }
  const int *renamed_tokens() const { return renamed_tokens_.data(); }
  const int *unique_tokens() const { return unique_tokens_.data(); }
  int num_tokens() const { return tokens_.size(); }
  int num_unique() const { return unique_tokens_.size(); }
  int num_twograms() const { return twogram_counts_.size(); }

  void Tokenize() {
      int token_start = 0;
      for (int pos = 0, end = size_; pos < end; ++pos) {
          char c = document_[pos];
          if (! IsTargetChar(c)) {
              if (pos - token_start > 0)
                  tokens_.emplace_back(token_start, pos - token_start);
              token_start = pos + 1;
          }
      }
      if (size_ - token_start > 0)
          tokens_.emplace_back(token_start, size_ - token_start);

      // for (auto &t: tokens_)
      //   tok_print(t), printf(" ");
      // printf("\n");
  }

  /**
  ArgsortTokens: calculate unique_tokens_, unique_token_counts_, renamed_tokens_

  Sort the tokens with tok_comp, and then using groupby to reduce it to unique
  tokens and counts; also, create a projection of the original document that
  replace each token with that token's rank in *unique*.
  */
  void ArgsortTokens() {
    int n_tokens = tokens_.size();
    if (n_tokens == 0) { return; }
    // unique_tokens_.clear(); // unique_token_counts_.clear();
    // renamed_tokens_.clear();
    renamed_tokens_.resize(n_tokens);
    vector<int> arg;
    arg.reserve(n_tokens);
    for (int i=0; i < n_tokens; ++i)
      arg.push_back(i);

    auto comp = [&](int x, int y) { return tok_comp(tokens_[x], tokens_[y]); };
    std::sort(arg.begin(), arg.end(), comp);

    typedef vector<int>::const_iterator ITER;
    auto each = [&](const ITER begin, const ITER end) {
      int new_name = unique_tokens_.size();
      int min = *begin;
      renamed_tokens_[*begin] = new_name;
      for (ITER i = begin + 1; i < end; ++i) {
        if (min > *i) { min = *i; }
        renamed_tokens_[*i] = new_name;
      }
      unique_tokens_.push_back(min);
      unique_token_counts_.push_back(end - begin);
    };
    auto eq = [&](int x, int y) { return tok_eq(tokens_[x], tokens_[y]); };
    groupby(arg.begin(), arg.end(), eq, each);
  }

  void MakeTwoGrams() {
    if (num_tokens() == 0) { return; }

    twograms_.clear();
    twograms_.reserve(renamed_tokens_.size());

    int x = renamed_tokens_[0];
    for (int i = 1, end = renamed_tokens_.size(); i < end; ++i) {
      int y = renamed_tokens_[i];
      twograms_.push_back({x, y});
      x = y;
    }
    std::sort(twograms_.begin(), twograms_.end());

    auto dest = twograms_.begin(), i = dest, j = i + 1;
    auto end = twograms_.end();
    for (; j < end; ++j) {
      if (*i == *j)
        continue;
      *dest = *i;
      int count = j - i;
      twogram_counts_.push_back(count);
      i = j;
      ++dest;
    }
    *dest = *i;
    int count = j - i;
    twogram_counts_.push_back(count);
    twograms_.resize(twogram_counts_.size());
  }

  void ShowUnique() const {
    for (int i = 0, end = unique_tokens_.size(); i < end; ++i)
      tok_print(tokens_[unique_tokens_[i]]),
      printf("(%d:%d) ", unique_tokens_[i], unique_token_counts_[i]);
    printf("\n");
  }

  void ShowRenamedTokens() const {
    for (int i: renamed_tokens_)
        tok_print(tokens_[unique_tokens_[i]]), printf("(%d) ", i);
    printf("\n");
  }

  void ShowTwoGrams() const {
    for (int i = 0, end = twograms_.size(); i < end; ++i) {
      auto &twogram = twograms_[i];
      for(int i: twogram)
        tok_print(tokens_[unique_tokens_[i]]), printf("(%d) ", i);
      printf(" %d\n", twogram_counts_[i]);
    }
  }

 private:
  const char *document_;
  int size_;
  int md5_[4];
  vector<Token> tokens_;
  vector<int> unique_tokens_;
  vector<int> unique_token_counts_;
  vector<int> renamed_tokens_;
  vector<array<int, 2>> twograms_;
  vector<int> twogram_counts_;
};

void document_analyse() {

}
