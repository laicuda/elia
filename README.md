# Elia - Easy E-Book License Assignment

Quite a number of schools buy their books in a dual license model.
This means, that they get a printed version of the book, which they can use many years, and moreover, a reduced-price ebook license can by bought by the school.
This license if usually valid for one year and mostly has to be paid by parents. Moreover, schools usually use books from several publishers.

As not all pupils and parents want to buy ebook licenses and at the same time, quite
a lot of pupils and parents want to buy such ebook licenses, I developed a series of
Python script that can help the school to manage the whole process in a semi-automated way.

**I developed these scripts *quick and very dirty* for me and my needs, so their usage is not at all ideal for others. But as some people asked me for an insight to what I did, I decided to provide them - and hope that ELIA also is helpful for others! :smiley:**

As I support a German school, this project is a mixture of German and English - sorry about that!

Our process is as follows - details on the steps can be found in the linked markdown files:

1. [School provides information on available ebooks](doc/A_provide_available_books.md)
2. [Parents answer a poll and thereby order ebook licenses](doc/B_parents_poll.md)
3. [Parents get an e-mail with payment information](doc/C_send_transfer_data.md)
4. Parents transfer money for the ebook licenses they ordered
5. [Number of ordered and paid licenses is counted](doc/D_analyse_payments.md)
6. School orders ebook licenses from publishers
7. [Parents get one or several e-mails containing ebook licenses and installation instructions from publishers](doc/E_send_licenses.md)
