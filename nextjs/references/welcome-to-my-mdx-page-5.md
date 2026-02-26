# Welcome to my MDX page!

export default function MDXPage({ children }) {
  return <MdxLayout>{children}</MdxLayout>

}
```

## Frontmatter

Frontmatter is a YAML like key/value pairing that can be used to store data about a page. `@next/mdx` does **not** support frontmatter by default, though there are many solutions for adding frontmatter to your MDX content, such as:

* [remark-frontmatter](https://github.com/remarkjs/remark-frontmatter)
* [remark-mdx-frontmatter](https://github.com/remcohaszing/remark-mdx-frontmatter)
* [gray-matter](https://github.com/jonschlinkert/gray-matter)

`@next/mdx` **does** allow you to use exports like any other JavaScript component:

```mdx filename="content/blog-post.mdx" switcher
export const metadata = {
  author: 'John Doe',
}