# Full-Stack-AI-apps

### Deploy AI to AWS, GCP, Azure, Vercel with MLOps, Bedrock, SageMaker, RAG, Agents, MCP: scalable, secure and observable.

# SaaS - Building a Full-Stack AI Application

## Build Your First SaaS Product with Next.js and FastAPI

Today you'll build a complete full-stack application with a React frontend and Python backend, all deployed to production on Vercel.

## What You'll Build

A **Business Idea Generator** - an AI-powered SaaS application that:

- Has a modern React frontend built with Next.js (using Pages Router for stability)
- Uses TypeScript for type safety
- Connects to a FastAPI backend
- Streams AI responses in real-time
- Renders beautiful Markdown content
- Deploys seamlessly to production

## Prerequisites

- Completed Day 1 (you should have Node.js and Vercel CLI installed)
- Your OpenAI API key from Day 1

## Step 1: Create Your Next.js Project

### Open Cursor and Create Your Project

1. Open Cursor
2. Open the terminal (Terminal → New Terminal or Ctrl+\` / Cmd+\`)
3. Navigate to your projects folder (or wherever you want to create the project)
4. Create a new Next.js project with TypeScript:

```bash
npx create-next-app@latest saas --typescript
```

When prompted, respond to each question:

1. **Which linter would you like to use?** → Press Enter for **ESLint** (default)
2. **Would you like to use Tailwind CSS?** → Type `y` and press Enter for **Yes**
3. **Would you like your code inside a `src/` directory?** → Type `n` and press Enter for **No**
4. **Would you like to use App Router? (recommended)** → Type `n` and press Enter for **No** (we're using Pages Router)
5. **Would you like to use Turbopack? (recommended)** → Type `n` and press Enter for **No** (we'll keep the standard build for compatibility)
6. **Would you like to customize the import alias?** → Type `n` and press Enter for **No**

This creates a new Next.js project with:

- **Pages Router** (the stable, battle-tested routing system)
- **TypeScript** for type safety
- **ESLint** for catching errors and enforcing code quality
- **Tailwind CSS** for utility-first styling

### Open Your Project

1. In Cursor: File → Open Folder → Select the "saas" folder that was just created
2. You'll see several files and folders that Next.js created automatically

### Understanding the Project Structure

Next.js created these key files and folders:

```
saas/
├── pages/              # Pages Router directory (where your pages live)
│   ├── _app.tsx       # Application wrapper (initializes pages)
│   ├── _document.tsx  # Custom document (HTML structure)
│   ├── index.tsx      # Homepage (routes to "/")
│   └── api/           # API routes directory (we'll remove this)
│       └── hello.ts   # Sample API route (we'll remove this)
├── styles/            # Styles directory
│   └── globals.css    # Global styles (includes Tailwind)
├── public/            # Static files (images, fonts, etc.)
├── package.json       # Node.js dependencies and scripts
├── tsconfig.json      # TypeScript configuration
├── next.config.js     # Next.js configuration
└── node_modules/      # Installed packages (auto-generated)
```

**Key files explained:**

- **`pages/_app.tsx`**: The application wrapper that initializes all pages. Used for global providers and styles
- **`pages/_document.tsx`**: Custom document for modifying the HTML structure
- **`pages/index.tsx`**: Your homepage component. This is what users see at "/"
- **`styles/globals.css`**: Global styles including Tailwind CSS imports

### Clean Up Unnecessary Files

Since we're using a Python FastAPI backend (not Next.js API routes), let's remove the sample API directory:

1. In Cursor's file explorer (left sidebar), find the `pages/api` folder
2. Right-click on the `api` folder
3. Select **Delete** (or press Delete/Backspace key)
4. Confirm the deletion when prompted

### What is Tailwind CSS?

**Tailwind CSS** is a utility-first CSS framework. Instead of writing custom CSS, you apply pre-built utility classes directly in your HTML/JSX. For example:

- `bg-blue-500` sets a blue background
- `text-white` makes text white
- `p-4` adds padding on all sides
- `rounded-lg` rounds the corners

This approach makes styling faster and more consistent!

## Step 2: Set Up the Backend

### Create the API Folder

In Cursor's file explorer, create a new folder at the root level:

- Right-click in the file explorer → New Folder → name it `api`

### Create Python Dependencies

Create a new file `requirements.txt` in the root directory with:

```
fastapi
uvicorn
openai
```

### Create the API Server

Create a new file `api/index.py`:

```python
from fastapi import FastAPI  # type: ignore
from fastapi.responses import PlainTextResponse  # type: ignore
from openai import OpenAI  # type: ignore

app = FastAPI()

@app.get("/api", response_class=PlainTextResponse)
def idea():
    client = OpenAI()
    prompt = [{"role": "user", "content": "Come up with a new business idea for AI Agents"}]
    response = client.chat.completions.create(model="gpt-5-nano", messages=prompt)
    return response.choices[0].message.content
```

## Step 3: Create Your First Page

### Understanding Client Components

In Next.js Pages Router, all page components run on both server and client by default. Since we're using a **Python/FastAPI backend** for our API (not Next.js's server), we'll mark our components with `"use client"` to ensure:

- The component runs in the browser
- The browser makes direct API calls to our Python backend
- We're not trying to use Next.js as a middleman server

### Create the Homepage

Replace the entire contents of `pages/index.tsx` with:

```typescript
"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [idea, setIdea] = useState<string>("…loading");

  useEffect(() => {
    fetch("/api")
      .then((res) => res.text())
      .then(setIdea)
      .catch((err) => setIdea("Error: " + err.message));
  }, []);

  return (
    <main className="p-8 font-sans">
      <h1 className="text-3xl font-bold mb-4">Business Idea Generator</h1>
      <div className="w-full max-w-2xl p-6 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm">
        <p className="text-gray-900 dark:text-gray-100 whitespace-pre-wrap">
          {idea}
        </p>
      </div>
    </main>
  );
}
```

**What's happening here:**

- `"use client"` tells Next.js this component runs in the browser
- The browser directly calls our Python FastAPI backend at `/api`
- We use React hooks to manage the UI state and fetch the data
- Vercel routes `/api` requests to our Python server (we don't need vercel.json configuration)

### Set Up the Application Wrapper

The `_app.tsx` file wraps all your pages. Let's create it to import our styles.

Create or replace `pages/_app.tsx` with:

```typescript
import type { AppProps } from "next/app";
import "../styles/globals.css"; // This imports Tailwind styles

export default function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}
```

### Set Up the Document

Now let's customize the HTML structure and add metadata.

Create `pages/_document.tsx`:

```typescript
import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <title>Business Idea Generator</title>
        <meta
          name="description"
          content="AI-powered business idea generation"
        />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
```

## Step 4: Configure Your Project

**Note:** We don't need a `vercel.json` file - Vercel automatically detects both Next.js and Python files in the `api` folder using its default configuration.

## Step 5: Link Your Project

First, let's create and link your Vercel project:

```bash
vercel link
```

Follow the prompts:

- Set up and link? → Yes
- Which scope? → Your personal account
- Link to existing project? → No
- What's the name of your project? → saas
- In which directory is your code located? → Current directory (press Enter)

This creates your Vercel project and links it to your local directory.

## Step 6: Add Your OpenAI API Key

Now that the project is created, add your OpenAI API key:

```bash
vercel env add OPENAI_API_KEY
```

- Paste your API key when prompted
- Select all environments (development, preview, production)

## Step 7: Deploy and Test

Deploy your application to test it:

```bash
vercel .
```

When prompted "Set up and deploy?", answer **No** (we already linked the project).

Visit the URL provided to see your Business Idea Generator loading an AI-generated idea!

**Note:** We test using the deployed version rather than local development, as this ensures both the Next.js frontend and Python backend work together properly.

## Step 8: Deploy to Production

Deploy your working application to production:

```bash
vercel --prod
```

Visit the URL provided to see your live application!

## Part 2: Add Real-Time Streaming

Now let's enhance your app with real-time streaming and Markdown rendering.

### Install Markdown Libraries

```bash
npm install react-markdown remark-gfm remark-breaks
```

### Update the Frontend

Replace `pages/index.tsx` with:

```typescript
"use client";

import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";

export default function Home() {
  const [idea, setIdea] = useState<string>("…loading");

  useEffect(() => {
    const evt = new EventSource("/api");
    let buffer = "";

    evt.onmessage = (e) => {
      buffer += e.data;
      setIdea(buffer);
    };
    evt.onerror = () => {
      console.error("SSE error, closing");
      evt.close();
    };

    return () => {
      evt.close();
    };
  }, []);

  return (
    <main className="p-8 font-sans">
      <h1 className="text-3xl font-bold mb-4">Business Idea Generator</h1>
      <div className="w-full max-w-2xl p-6 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg shadow-md">
        <div className="prose prose-gray dark:prose-invert max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm, remarkBreaks]}>
            {idea}
          </ReactMarkdown>
        </div>
      </div>
    </main>
  );
}
```

**Tailwind classes explained:**

- `prose`: Tailwind Typography plugin class that styles markdown content beautifully
- `w-full max-w-2xl`: Full width with a maximum width constraint
- `p-6`: Padding on all sides
- `bg-gray-50`: Light gray background
- `border border-gray-200`: Border with gray color
- `rounded-lg`: Rounded corners

**Note:** We still need `"use client"` at the top because we're making direct API calls from the browser to our Python FastAPI backend (rather than using Next.js as a middleman server).

### Install Tailwind Typography Plugin

The `prose` class requires the Typography plugin. Install it:

```bash
npm install @tailwindcss/typography
```

### Update the Backend for Streaming

Replace `api/index.py` with:

```python
from fastapi import FastAPI  # type: ignore
from fastapi.responses import StreamingResponse  # type: ignore
from openai import OpenAI  # type: ignore

app = FastAPI()

@app.get("/api")
def idea():
    client = OpenAI()
    prompt = [{"role": "user", "content": "Come up with a new business idea for AI Agents"}]
    stream = client.chat.completions.create(model="gpt-5-nano", messages=prompt, stream=True)

    def event_stream():
        for chunk in stream:
            text = chunk.choices[0].delta.content
            if text:
                lines = text.split("\n")
                for line in lines:
                    yield f"data: {line}\n"
                yield "\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

### Test Streaming

Deploy and test your updated application:

```bash
vercel .
```

Visit the URL provided. You'll now see the AI response streaming in real-time with proper Markdown formatting!

## Part 3: Professional Styling

Let's make your app look professional with modern styling.

### Fix Markdown Rendering

First, we need to restore the default HTML styles that Tailwind removes. Add this to the bottom of your `styles/globals.css` file:

```css
@layer base {
  .markdown-content h1 {
    font-size: 2em;
    font-weight: bold;
    margin: 0.67em 0;
  }
  .markdown-content h2 {
    font-size: 1.5em;
    font-weight: bold;
    margin: 0.83em 0;
  }
  .markdown-content h3 {
    font-size: 1.17em;
    font-weight: bold;
    margin: 1em 0;
  }
  .markdown-content h4 {
    font-size: 1em;
    font-weight: bold;
    margin: 1.33em 0;
  }
  .markdown-content h5 {
    font-size: 0.83em;
    font-weight: bold;
    margin: 1.67em 0;
  }
  .markdown-content h6 {
    font-size: 0.67em;
    font-weight: bold;
    margin: 2.33em 0;
  }
  .markdown-content p {
    margin: 1em 0;
  }
  .markdown-content ul {
    list-style-type: disc;
    padding-left: 2em;
    margin: 1em 0;
  }
  .markdown-content ol {
    list-style-type: decimal;
    padding-left: 2em;
    margin: 1em 0;
  }
  .markdown-content li {
    margin: 0.25em 0;
  }
  .markdown-content strong {
    font-weight: bold;
  }
  .markdown-content em {
    font-style: italic;
  }
  .markdown-content hr {
    border: 0;
    border-top: 1px solid #e5e7eb;
    margin: 2em 0;
  }
}
```

### Update Your Backend Prompt

Update the prompt in `api/index.py` to request formatted output:

```python
prompt = [{"role": "user", "content": "Reply with a new business idea for AI Agents, formatted with headings, sub-headings and bullet points"}]
```

### Update Your Component

Now replace `pages/index.tsx` with:

```typescript
"use client";

import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";

export default function Home() {
  const [idea, setIdea] = useState<string>("…loading");

  useEffect(() => {
    const evt = new EventSource("/api");
    let buffer = "";

    evt.onmessage = (e) => {
      buffer += e.data;
      setIdea(buffer);
    };
    evt.onerror = () => {
      console.error("SSE error, closing");
      evt.close();
    };

    return () => {
      evt.close();
    };
  }, []);

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
            Business Idea Generator
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            AI-powered innovation at your fingertips
          </p>
        </header>

        {/* Content Card */}
        <div className="max-w-3xl mx-auto">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 backdrop-blur-lg bg-opacity-95">
            {idea === "…loading" ? (
              <div className="flex items-center justify-center py-12">
                <div className="animate-pulse text-gray-400">
                  Generating your business idea...
                </div>
              </div>
            ) : (
              <div className="markdown-content text-gray-700 dark:text-gray-300">
                <ReactMarkdown remarkPlugins={[remarkGfm, remarkBreaks]}>
                  {idea}
                </ReactMarkdown>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
```

**Professional Tailwind styling:**

- `min-h-screen`: Full viewport height
- `bg-gradient-to-br`: Beautiful gradient background with dark mode support
- `container mx-auto`: Centered container with responsive padding
- `text-5xl font-bold bg-gradient-to-r bg-clip-text text-transparent`: Gradient text effect for the heading
- `rounded-2xl shadow-xl backdrop-blur-lg`: Modern glassmorphism card effect
- `animate-pulse`: Loading animation while content streams
- `markdown-content`: Custom class that restores HTML styling for markdown

## Step 9: Deploy Final Version

Deploy your enhanced application:

```bash
vercel --prod
```

## Congratulations! 🎉

You've built a complete SaaS application with:

- ✅ Modern React frontend with Next.js Pages Router
- ✅ TypeScript for type safety
- ✅ FastAPI Python backend
- ✅ Real-time streaming AI responses
- ✅ Beautiful Markdown rendering
- ✅ Professional styling
- ✅ Production deployment on Vercel

## What You've Learned

- How to structure a full-stack application
- Building with Next.js Pages Router
- Understanding client-side rendering for API calls
- Creating API endpoints with FastAPI
- Implementing Server-Sent Events for streaming
- Rendering Markdown content in React
- Deploying full-stack apps to Vercel

## Understanding Pages Router Concepts

**Pages Router Structure:**

- Each file in `pages/` becomes a route
- `pages/index.tsx` → `/`
- `pages/product.tsx` → `/product`
- `pages/api/` → API routes (though we're using Python instead)

**Client-Side Rendering (`"use client"`):**

- Components marked with `"use client"` run primarily in the browser
- Can use React hooks (useState, useEffect)
- Perfect for dynamic, interactive UI
- We use this for all our pages since we're calling a Python backend

In this project, we used client-side components because we needed browser features for real-time streaming and connecting to our FastAPI backend.

## Next Steps

- Add a button to generate new ideas
- Store ideas in a database
- Add user authentication
- Create different idea categories
- Add a copy-to-clipboard feature
- Implement idea saving and sharing

## Troubleshooting

### "Module not found" errors

- Make sure you've installed all npm packages
- Try deleting `node_modules` and running `npm install` again

### API not responding

- Check that your OpenAI API key is set correctly
- Verify you have credits in your OpenAI account

### Streaming not working

- Some browsers block SSE on localhost - try a different browser
- Check the browser console for errors

### ESLint warnings

- ESLint helps catch potential issues in your code
- Yellow squiggly lines are warnings (code will still run)
- Red squiggly lines are errors (should be fixed)
- You can temporarily disable ESLint for a line with `// eslint-disable-next-line`
- Common warnings:
  - "React Hook useEffect has missing dependencies" - Usually safe to ignore for simple demos
  - "Unused variable" - Remove variables you're not using

### TypeScript errors

- Ensure all TypeScript packages are installed
- Restart your development server after installing types

### Deployment issues

- Make sure all files are saved before deploying
- Check that vercel.json is properly formatted
- Ensure your API key is added to Vercel environment variables

# Day 3: Adding User Authentication with Clerk

## Transform Your SaaS with Professional Authentication

Today you'll add enterprise-grade authentication to your Business Idea Generator, allowing users to sign in with Google, GitHub, and other providers. This transforms your app from a demo into a real SaaS product.

## What You'll Build

An authenticated version of your app that:

- Requires users to sign in before accessing the idea generator
- Supports multiple authentication providers (Google, GitHub, Email)
- Passes secure JWT tokens to your backend
- Verifies user identity on every API request
- Works seamlessly with Next.js Pages Router

## Prerequisites

- Completed Day 2 (working Business Idea Generator)
- Your project deployed to Vercel

## Part 1: User Authentication

### Step 1: Create Your Clerk Account

1. Visit [clerk.com](https://clerk.com) and click **Sign Up**
2. Create your account using Google auth (or your preferred method)
3. You'll be taken to **Create Application** (or click "Create Application" if returning)

### Step 2: Configure Your Clerk Application

1. **Application name:** SaaS
2. **Sign-in options:** Enable these providers:
   - Email
   - Google
   - GitHub
   - Apple (optional)
3. Click **Create Application**

You'll see the Clerk dashboard with your API keys displayed.

### Step 3: Install Clerk Dependencies

In your terminal, install the Clerk SDK:

```bash
npm install @clerk/nextjs
```

For handling streaming with authentication, also install:

```bash
npm install @microsoft/fetch-event-source
```

### Step 4: Configure Environment Variables

Create a `.env.local` file in your project root:

```bash
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_publishable_key_here
CLERK_SECRET_KEY=your_secret_key_here
```

**Important:** Copy these values from the Clerk dashboard (they're displayed after creating your application on the configure screen).

### Add to .gitignore

Open `.gitignore` in Cursor and add `.env.local` on a new line.

### Step 5: Add Clerk Provider to Your App

With Pages Router, we need to wrap our application with the Clerk provider. Update `pages/_app.tsx`:

```typescript
import { ClerkProvider } from "@clerk/nextjs";
import type { AppProps } from "next/app";
import "../styles/globals.css";

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ClerkProvider {...pageProps}>
      <Component {...pageProps} />
    </ClerkProvider>
  );
}
```

### Step 6: Create the Product Page

Move your business idea generator to a protected route. Since we're using client-side authentication, we'll protect this route using Clerk's built-in components.

Create `pages/product.tsx`:

```typescript
"use client";

import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";
import { useAuth } from "@clerk/nextjs";
import { fetchEventSource } from "@microsoft/fetch-event-source";

export default function Product() {
  const { getToken } = useAuth();
  const [idea, setIdea] = useState<string>("…loading");

  useEffect(() => {
    let buffer = "";
    (async () => {
      const jwt = await getToken();
      if (!jwt) {
        setIdea("Authentication required");
        return;
      }

      await fetchEventSource("/api", {
        headers: { Authorization: `Bearer ${jwt}` },
        onmessage(ev) {
          buffer += ev.data;
          setIdea(buffer);
        },
        onerror(err) {
          console.error("SSE error:", err);
          // Don't throw - let it retry
        },
      });
    })();
  }, []); // Empty dependency array - run once on mount

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
            Business Idea Generator
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            AI-powered innovation at your fingertips
          </p>
        </header>

        {/* Content Card */}
        <div className="max-w-3xl mx-auto">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 backdrop-blur-lg bg-opacity-95">
            {idea === "…loading" ? (
              <div className="flex items-center justify-center py-12">
                <div className="animate-pulse text-gray-400">
                  Generating your business idea...
                </div>
              </div>
            ) : (
              <div className="markdown-content text-gray-700 dark:text-gray-300">
                <ReactMarkdown remarkPlugins={[remarkGfm, remarkBreaks]}>
                  {idea}
                </ReactMarkdown>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
```

### Step 7: Create the Landing Page

Update `pages/index.tsx` to be your new landing page with sign-in:

```typescript
"use client";

import Link from "next/link";
import { SignInButton, SignedIn, SignedOut, UserButton } from "@clerk/nextjs";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-12">
        {/* Navigation */}
        <nav className="flex justify-between items-center mb-12">
          <h1 className="text-2xl font-bold text-gray-800 dark:text-gray-200">
            IdeaGen
          </h1>
          <div>
            <SignedOut>
              <SignInButton mode="modal">
                <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors">
                  Sign In
                </button>
              </SignInButton>
            </SignedOut>
            <SignedIn>
              <div className="flex items-center gap-4">
                <Link
                  href="/product"
                  className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
                >
                  Go to App
                </Link>
                <UserButton afterSignOutUrl="/" />
              </div>
            </SignedIn>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="text-center py-24">
          <h2 className="text-6xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-6">
            Generate Your Next
            <br />
            Big Business Idea
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-12 max-w-2xl mx-auto">
            Harness the power of AI to discover innovative business
            opportunities tailored for the AI agent economy
          </p>

          <SignedOut>
            <SignInButton mode="modal">
              <button className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-4 px-8 rounded-xl text-lg transition-all transform hover:scale-105">
                Get Started Free
              </button>
            </SignInButton>
          </SignedOut>
          <SignedIn>
            <Link href="/product">
              <button className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-4 px-8 rounded-xl text-lg transition-all transform hover:scale-105">
                Generate Ideas Now
              </button>
            </Link>
          </SignedIn>
        </div>
      </div>
    </main>
  );
}
```

### Step 8: Configure Backend Authentication

First, get your JWKS URL from Clerk:

1. Go to your Clerk Dashboard
2. Click **Configure** (top nav)
3. Click **API Keys** (side nav)
4. Find **JWKS URL** and copy it

**What is JWKS?** The JWKS (JSON Web Key Set) URL is a public endpoint that contains Clerk's public keys. When a user signs in, Clerk creates a JWT (JSON Web Token) - a digitally signed token that proves the user's identity. Your Python backend uses the JWKS URL to fetch Clerk's public keys and verify that incoming JWT tokens are genuine and haven't been tampered with. This allows secure authentication without your backend needing to contact Clerk for every request - it can verify tokens independently using cryptographic signatures.

Add to `.env.local`:

```bash
CLERK_JWKS_URL=your_jwks_url_here
```

### Step 9: Update Backend Dependencies

Add the Clerk authentication library to `requirements.txt`:

```
fastapi
uvicorn
openai
fastapi-clerk-auth
```

### Step 10: Update the API with Authentication

Replace `api/index.py` with:

```python
import os
from fastapi import FastAPI, Depends  # type: ignore
from fastapi.responses import StreamingResponse  # type: ignore
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer, HTTPAuthorizationCredentials  # type: ignore
from openai import OpenAI  # type: ignore

app = FastAPI()

clerk_config = ClerkConfig(jwks_url=os.getenv("CLERK_JWKS_URL"))
clerk_guard = ClerkHTTPBearer(clerk_config)

@app.get("/api")
def idea(creds: HTTPAuthorizationCredentials = Depends(clerk_guard)):
    user_id = creds.decoded["sub"]  # User ID from JWT - available for future use
    # We now know which user is making the request!
    # You could use user_id to:
    # - Track usage per user
    # - Store generated ideas in a database
    # - Apply user-specific limits or customization

    client = OpenAI()
    prompt = [{"role": "user", "content": "Reply with a new business idea for AI Agents, formatted with headings, sub-headings and bullet points"}]
    stream = client.chat.completions.create(model="gpt-5-nano", messages=prompt, stream=True)

    def event_stream():
        for chunk in stream:
            text = chunk.choices[0].delta.content
            if text:
                lines = text.split("\n")
                for line in lines[:-1]:
                    yield f"data: {line}\n\n"
                    yield "data:  \n"
                yield f"data: {lines[-1]}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

### Step 11: Add Environment Variables to Vercel

Add your Clerk keys to Vercel:

```bash
vercel env add NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
```

Paste your publishable key and select all environments.

```bash
vercel env add CLERK_SECRET_KEY
```

Paste your secret key and select all environments.

```bash
vercel env add CLERK_JWKS_URL
```

Paste your JWKS URL and select all environments.

### Step 12: Test Locally

Test your authentication locally:

```bash
vercel dev
```

**Note:** The Python backend won't work locally with `vercel dev`, but the authentication flow will work perfectly! You'll be able to sign in, sign out, and see the user interface.

Visit `http://localhost:3000` and:

1. Click "Sign In"
2. Create an account or sign in with Google/GitHub
3. You'll be redirected to the landing page, now authenticated
4. Click "Go to App" to access the protected idea generator

### Step 13: Deploy to Production

Deploy your authenticated app:

```bash
vercel --prod
```

Visit your production URL and test the complete authentication flow!

NOTE - if you hit a problem with jwt token expiration, please see this [fix contributed by Artur P](../community_contributions/arturp_jwt_token_fix_notes.md)

## What's Happening?

Your app now has:

- **Secure authentication**: Users must sign in to access your product
- **Client-side route protection**: Unauthenticated users are redirected from protected pages
- **JWT verification**: Every API request is verified using cryptographic signatures
- **User identification**: The backend knows which user is making each request
- **Professional UX**: Modal sign-in, user profile management, and smooth redirects
- **Multiple providers**: Users can choose their preferred sign-in method

## Security Architecture

Since we're using client-side Next.js with a separate Python backend:

1. **Frontend (Browser)**: User signs in with Clerk → receives session token
2. **Client-Side Protection**: Protected routes check authentication status and redirect if needed
3. **API Request**: Browser sends JWT token directly to Python backend with each request
4. **Backend Verification**: FastAPI verifies the JWT using Clerk's public keys (JWKS)
5. **User Context**: Backend can access user ID and metadata from verified token

This architecture keeps your Next.js deployment simple (static/client-side only) while maintaining secure API authentication.

## Troubleshooting

### "Unauthorized" errors

- Check that all three environment variables are set correctly in Vercel
- Ensure the JWKS URL is copied correctly from Clerk
- Verify you're signed in before accessing `/product`

### Sign-in modal not appearing

- Check that `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` starts with `pk_`
- Ensure you've wrapped your app with `ClerkProvider`
- Clear browser cache and cookies

### API not authenticating

- Verify `CLERK_JWKS_URL` is set in your environment
- Check that `fastapi-clerk-auth` is in requirements.txt
- Ensure the JWT token is being sent in the Authorization header

### Local development issues

- Make sure `.env.local` has all three Clerk variables
- Restart your dev server after adding environment variables
- Try clearing Next.js cache: `rm -rf .next`

## Next Steps

Congratulations! You've added professional authentication to your SaaS. In Part 2, we'll add:

- Subscription tiers with Stripe
- Usage limits based on subscription level
- Payment processing
- Customer portal for managing subscriptions

Your app is now a real SaaS product with secure user authentication!

# Day 3 Part 2: Adding Subscriptions with Clerk Billing

## Transform Your SaaS with Subscription Management

Now let's add subscription tiers to your Business Idea Generator, turning it into a full-fledged SaaS with payment processing and subscription management built-in.

## What You'll Build

An enhanced version of your app that:

- Requires a paid subscription to access the idea generator
- Shows a beautiful pricing table to non-subscribers
- Handles payment processing through Clerk Billing
- Manages subscription status automatically
- Provides a user menu with billing management options

## Prerequisites

- Completed Day 3 Part 1 (authentication working)
- Your app deployed to Vercel

## Step 1: Enable Clerk Billing

### Navigate to Clerk Dashboard

1. Go to your [Clerk Dashboard](https://dashboard.clerk.com)
2. Select your **SaaS** application
3. Click **Configure** in the top navigation
4. Click **Subscription Plans** in the left sidebar
5. Click **Get Started** if this is your first time

### Enable Billing

1. Click **Enable Billing** if prompted
2. Accept the terms if prompted
3. You'll see the Subscription Plans page

## Step 2: Create Your Subscription Plan

### Configure the Plan

1. Click **Create Plan**
2. Fill in the details:
   - **Name:** Premium Subscription
   - **Key:** `premium_subscription` (this is important - copy it exactly)
   - **Price:** $10.00 monthly (or your preferred price)
   - **Description:** Unlimited AI-powered business ideas
3. Optional: Add an annual discount
   - Toggle on **Annual billing**
   - Set annual price (e.g., $100/year for a discount)
4. Click **Save**

### Copy the Plan ID

After creating the plan, you'll see a **Plan ID** in the top right of the plan card (it looks like `plan_...`). You'll need this for testing, but Clerk handles it automatically in production.

## Step 3: Update Your Product Page

Since we're using Pages Router with client-side components, we need to protect our product route with the subscription check.

Update `pages/product.tsx`:

```typescript
"use client";

import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";
import { useAuth } from "@clerk/nextjs";
import { fetchEventSource } from "@microsoft/fetch-event-source";
import { Protect, PricingTable, UserButton } from "@clerk/nextjs";

function IdeaGenerator() {
  const { getToken } = useAuth();
  const [idea, setIdea] = useState<string>("…loading");

  useEffect(() => {
    let buffer = "";
    (async () => {
      const jwt = await getToken();
      if (!jwt) {
        setIdea("Authentication required");
        return;
      }

      await fetchEventSource("/api", {
        headers: { Authorization: `Bearer ${jwt}` },
        onmessage(ev) {
          buffer += ev.data;
          setIdea(buffer);
        },
        onerror(err) {
          console.error("SSE error:", err);
          // Don't throw - let it retry
        },
      });
    })();
  }, []); // Empty dependency array - run once on mount

  return (
    <div className="container mx-auto px-4 py-12">
      {/* Header */}
      <header className="text-center mb-12">
        <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
          Business Idea Generator
        </h1>
        <p className="text-gray-600 dark:text-gray-400 text-lg">
          AI-powered innovation at your fingertips
        </p>
      </header>

      {/* Content Card */}
      <div className="max-w-3xl mx-auto">
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 backdrop-blur-lg bg-opacity-95">
          {idea === "…loading" ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-pulse text-gray-400">
                Generating your business idea...
              </div>
            </div>
          ) : (
            <div className="markdown-content text-gray-700 dark:text-gray-300">
              <ReactMarkdown remarkPlugins={[remarkGfm, remarkBreaks]}>
                {idea}
              </ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function Product() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      {/* User Menu in Top Right */}
      <div className="absolute top-4 right-4">
        <UserButton showName={true} />
      </div>

      {/* Subscription Protection */}
      <Protect
        plan="premium_subscription"
        fallback={
          <div className="container mx-auto px-4 py-12">
            <header className="text-center mb-12">
              <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
                Choose Your Plan
              </h1>
              <p className="text-gray-600 dark:text-gray-400 text-lg mb-8">
                Unlock unlimited AI-powered business ideas
              </p>
            </header>
            <div className="max-w-4xl mx-auto">
              <PricingTable />
            </div>
          </div>
        }
      >
        <IdeaGenerator />
      </Protect>
    </main>
  );
}
```

## Step 4: Update Your Landing Page

Let's update the landing page to better reflect the subscription model.

Update `pages/index.tsx`:

```typescript
"use client";

import Link from "next/link";
import { SignInButton, SignedIn, SignedOut, UserButton } from "@clerk/nextjs";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-12">
        {/* Navigation */}
        <nav className="flex justify-between items-center mb-12">
          <h1 className="text-2xl font-bold text-gray-800 dark:text-gray-200">
            IdeaGen Pro
          </h1>
          <div>
            <SignedOut>
              <SignInButton mode="modal">
                <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors">
                  Sign In
                </button>
              </SignInButton>
            </SignedOut>
            <SignedIn>
              <div className="flex items-center gap-4">
                <Link
                  href="/product"
                  className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
                >
                  Go to App
                </Link>
                <UserButton showName={true} />
              </div>
            </SignedIn>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="text-center py-24">
          <h2 className="text-6xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-6">
            Generate Your Next
            <br />
            Big Business Idea
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-2xl mx-auto">
            Harness the power of AI to discover innovative business
            opportunities tailored for the AI agent economy
          </p>

          {/* Pricing Preview */}
          <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-lg rounded-xl p-6 max-w-sm mx-auto mb-8">
            <h3 className="text-2xl font-bold mb-2">Premium Subscription</h3>
            <p className="text-4xl font-bold text-blue-600 mb-2">
              $10<span className="text-lg text-gray-600">/month</span>
            </p>
            <ul className="text-left text-gray-600 dark:text-gray-400 mb-6">
              <li className="mb-2">✓ Unlimited idea generation</li>
              <li className="mb-2">✓ Advanced AI models</li>
              <li className="mb-2">✓ Priority support</li>
            </ul>
          </div>

          <SignedOut>
            <SignInButton mode="modal">
              <button className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-4 px-8 rounded-xl text-lg transition-all transform hover:scale-105">
                Start Your Free Trial
              </button>
            </SignInButton>
          </SignedOut>
          <SignedIn>
            <Link href="/product">
              <button className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-4 px-8 rounded-xl text-lg transition-all transform hover:scale-105">
                Access Premium Features
              </button>
            </Link>
          </SignedIn>
        </div>
      </div>
    </main>
  );
}
```

## Step 5: Configure Billing Provider (Optional)

Clerk comes with a built-in payment gateway that's ready to use immediately:

1. In Clerk Dashboard → **Configure** → **Billing** → **Settings** (in the left sidebar)
2. By default, **Clerk payment gateway** is selected:
   - "Our zero-config payment gateway. Ready to process test payments immediately."
   - This works great for testing and development
3. **Optional:** You can switch to Stripe if you prefer:
   - Select **Stripe** instead
   - Follow Clerk's setup wizard to connect your Stripe account

**Note:** The Clerk payment gateway is perfect for getting started - it handles test payments immediately without any additional setup.

## Step 6: Test Your Subscription Flow

Deploy your updated application:

```bash
vercel --prod
```

### Testing the Flow

1. Visit your production URL
2. Sign in (or create a new account)
3. Click "Go to App" or "Access Premium Features"
4. You'll see the pricing table since you don't have a subscription
5. Click **Subscribe** on the Premium plan
6. If you haven't connected a payment provider, Clerk will simulate the subscription
7. After subscribing, you'll have access to the idea generator

### Managing Subscriptions

Users can manage their subscriptions through the UserButton menu:

1. Click on their profile picture (UserButton)
2. Select **Manage account**
3. Navigate to **Subscriptions**
4. View or cancel their subscription

## What's Happening?

Your app now has:

- **Subscription Gate**: Users must have an active subscription to access the product
- **Pricing Table**: Beautiful, Clerk-managed pricing display
- **Payment Processing**: Handled entirely by Clerk (with Stripe integration if configured)
- **User Management**: Subscription status in the UserButton menu
- **Automatic Enforcement**: Clerk automatically checks subscription status

## Architecture Overview

1. **User visits `/product`** → Clerk checks subscription status
2. **No subscription** → Shows PricingTable component
3. **Has subscription** → Shows IdeaGenerator component
4. **Payment** → Handled by Clerk Billing (optionally with Stripe)
5. **Management** → Users manage subscriptions through Clerk's UI

## Troubleshooting

### "Plan not found" error

- Ensure the plan key is exactly `premium_subscription`
- Check that billing is enabled in Clerk Dashboard
- Verify the plan is active (not archived)

### Pricing table not showing

- Clear browser cache and cookies
- Check that `@clerk/nextjs` is up to date
- Ensure billing is enabled in your Clerk application

### Always seeing the pricing table (even after subscribing)

- Check the user's subscription status in Clerk Dashboard
- Verify the plan key matches exactly
- Try signing out and back in

### Payment not working

- This is normal if you haven't connected a payment provider
- Clerk will simulate subscriptions in test mode
- For real payments, connect Stripe in Billing Settings

## Customization Options

### Different Plan Tiers

You can create multiple plans in Clerk Dashboard:

```typescript
<Protect
  plan={["basic_plan", "premium_plan", "enterprise_plan"]}
  fallback={<PricingTable />}
>
  <IdeaGenerator />
</Protect>
```

### Custom Pricing Table

Instead of Clerk's default PricingTable, you can build your own:

```typescript
<Protect plan="premium_subscription" fallback={<CustomPricingPage />}>
  <IdeaGenerator />
</Protect>
```

### Usage Limits

Track API usage per user in your backend:

```python
@app.get("/api")
def idea(creds: HTTPAuthorizationCredentials = Depends(clerk_guard)):
    user_id = creds.decoded["sub"]
    subscription_plan = creds.decoded.get("subscription", "free")

    # Apply different limits based on plan
    if subscription_plan == "premium_subscription":
        # Unlimited or high limit
        pass
    else:
        # Limited access
        pass
```

## Next Steps

Congratulations! You've built a complete SaaS with:

- ✅ User authentication
- ✅ Subscription management
- ✅ Payment processing
- ✅ AI-powered features
- ✅ Professional UI/UX

### Ideas for Enhancement

1. **Multiple subscription tiers** (Basic, Pro, Enterprise)
2. **Usage tracking** and limits per tier
3. **Webhook integration** for subscription events
4. **Email notifications** for subscription changes
5. **Admin dashboard** to manage users and subscriptions
6. **Annual billing discounts**
7. **Free trial periods**

Your Business Idea Generator is now a fully-functional SaaS product ready for real customers!

# Day 4: Healthcare Consultation Assistant

## Build a Professional Healthcare Application

Today, you'll transform your SaaS into a healthcare consultation assistant that helps doctors generate patient summaries, action items, and patient-friendly emails from their visit notes.

## What You'll Build

A healthcare application that:

- Takes doctor's consultation notes as input
- Generates professional summaries for medical records
- Creates actionable next steps for the doctor
- Drafts patient-friendly email communications
- Uses structured forms with date pickers
- Streams AI-generated content in real-time

## Prerequisites

- Completed Day 3 (authentication and subscriptions working)
- Your app deployed to Vercel

## Step 1: Install Additional Dependencies

We need a date picker for the consultation form:

```bash
npm install react-datepicker
npm install --save-dev @types/react-datepicker
```

## Step 2: Update the Backend API

Replace `api/index.py` with a new endpoint that handles consultation data:

```python
import os
from fastapi import FastAPI, Depends  # type: ignore
from fastapi.responses import StreamingResponse  # type: ignore
from pydantic import BaseModel  # type: ignore
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer, HTTPAuthorizationCredentials  # type: ignore
from openai import OpenAI  # type: ignore

app = FastAPI()
clerk_config = ClerkConfig(jwks_url=os.getenv("CLERK_JWKS_URL"))
clerk_guard = ClerkHTTPBearer(clerk_config)


class Visit(BaseModel):
    patient_name: str
    date_of_visit: str
    notes: str


system_prompt = """
You are provided with notes written by a doctor from a patient's visit.
Your job is to summarize the visit for the doctor and provide an email.
Reply with exactly three sections with the headings:
### Summary of visit for the doctor's records
### Next steps for the doctor
### Draft of email to patient in patient-friendly language
"""


def user_prompt_for(visit: Visit) -> str:
    return f"""Create the summary, next steps and draft email for:
Patient Name: {visit.patient_name}
Date of Visit: {visit.date_of_visit}
Notes:
{visit.notes}"""


@app.post("/api")
def consultation_summary(
    visit: Visit,
    creds: HTTPAuthorizationCredentials = Depends(clerk_guard),
):
    user_id = creds.decoded["sub"]  # Available for tracking/auditing
    client = OpenAI()

    user_prompt = user_prompt_for(visit)

    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    stream = client.chat.completions.create(
        model="gpt-5-nano",
        messages=prompt,
        stream=True,
    )

    def event_stream():
        for chunk in stream:
            text = chunk.choices[0].delta.content
            if text:
                lines = text.split("\n")
                for line in lines[:-1]:
                    yield f"data: {line}\n\n"
                    yield "data:  \n"
                yield f"data: {lines[-1]}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

Note the key changes:

- Changed from `@app.get("/api")` to `@app.post("/api")` to accept form data
- Added a `Visit` model to validate incoming data
- Structured prompts for healthcare-specific output

## Step 3: Update Application Configuration

First, import the date picker styles in `pages/_app.tsx`:

```typescript
import { ClerkProvider } from "@clerk/nextjs";
import type { AppProps } from "next/app";
import "react-datepicker/dist/react-datepicker.css";
import "../styles/globals.css";

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ClerkProvider {...pageProps}>
      <Component {...pageProps} />
    </ClerkProvider>
  );
}
```

Now update `pages/_document.tsx` to reflect the healthcare focus:

```typescript
import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <title>Healthcare Consultation Assistant</title>
        <meta
          name="description"
          content="AI-powered medical consultation summaries"
        />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
```

## Step 4: Create the Consultation Form

Replace `pages/product.tsx` with the new healthcare interface:

```typescript
"use client";

import { useState, FormEvent } from "react";
import { useAuth } from "@clerk/nextjs";
import DatePicker from "react-datepicker";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";
import { fetchEventSource } from "@microsoft/fetch-event-source";
import { Protect, PricingTable, UserButton } from "@clerk/nextjs";

function ConsultationForm() {
  const { getToken } = useAuth();

  // Form state
  const [patientName, setPatientName] = useState("");
  const [visitDate, setVisitDate] = useState<Date | null>(new Date());
  const [notes, setNotes] = useState("");

  // Streaming state
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setOutput("");
    setLoading(true);

    const jwt = await getToken();
    if (!jwt) {
      setOutput("Authentication required");
      setLoading(false);
      return;
    }

    const controller = new AbortController();
    let buffer = "";

    await fetchEventSource("/api", {
      signal: controller.signal,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${jwt}`,
      },
      body: JSON.stringify({
        patient_name: patientName,
        date_of_visit: visitDate?.toISOString().slice(0, 10),
        notes,
      }),
      onmessage(ev) {
        buffer += ev.data;
        setOutput(buffer);
      },
      onclose() {
        setLoading(false);
      },
      onerror(err) {
        console.error("SSE error:", err);
        controller.abort();
        setLoading(false);
      },
    });
  }

  return (
    <div className="container mx-auto px-4 py-12 max-w-3xl">
      <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100 mb-8">
        Consultation Notes
      </h1>

      <form
        onSubmit={handleSubmit}
        className="space-y-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8"
      >
        <div className="space-y-2">
          <label
            htmlFor="patient"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Patient Name
          </label>
          <input
            id="patient"
            type="text"
            required
            value={patientName}
            onChange={(e) => setPatientName(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            placeholder="Enter patient's full name"
          />
        </div>

        <div className="space-y-2">
          <label
            htmlFor="date"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Date of Visit
          </label>
          <DatePicker
            id="date"
            selected={visitDate}
            onChange={(d: Date | null) => setVisitDate(d)}
            dateFormat="yyyy-MM-dd"
            placeholderText="Select date"
            required
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
          />
        </div>

        <div className="space-y-2">
          <label
            htmlFor="notes"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Consultation Notes
          </label>
          <textarea
            id="notes"
            required
            rows={8}
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            placeholder="Enter detailed consultation notes..."
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200"
        >
          {loading ? "Generating Summary..." : "Generate Summary"}
        </button>
      </form>

      {output && (
        <section className="mt-8 bg-gray-50 dark:bg-gray-800 rounded-xl shadow-lg p-8">
          <div className="markdown-content prose prose-blue dark:prose-invert max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm, remarkBreaks]}>
              {output}
            </ReactMarkdown>
          </div>
        </section>
      )}
    </div>
  );
}

export default function Product() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      {/* User Menu in Top Right */}
      <div className="absolute top-4 right-4">
        <UserButton showName={true} />
      </div>

      {/* Subscription Protection */}
      <Protect
        plan="premium_subscription"
        fallback={
          <div className="container mx-auto px-4 py-12">
            <header className="text-center mb-12">
              <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
                Healthcare Professional Plan
              </h1>
              <p className="text-gray-600 dark:text-gray-400 text-lg mb-8">
                Streamline your patient consultations with AI-powered summaries
              </p>
            </header>
            <div className="max-w-4xl mx-auto">
              <PricingTable />
            </div>
          </div>
        }
      >
        <ConsultationForm />
      </Protect>
    </main>
  );
}
```

## Step 5: Update the Landing Page

Update `pages/index.tsx` to reflect the healthcare focus:

```typescript
"use client";

import Link from "next/link";
import { SignInButton, SignedIn, SignedOut, UserButton } from "@clerk/nextjs";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-12">
        {/* Navigation */}
        <nav className="flex justify-between items-center mb-12">
          <h1 className="text-2xl font-bold text-gray-800 dark:text-gray-200">
            MediNotes Pro
          </h1>
          <div>
            <SignedOut>
              <SignInButton mode="modal">
                <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors">
                  Sign In
                </button>
              </SignInButton>
            </SignedOut>
            <SignedIn>
              <div className="flex items-center gap-4">
                <Link
                  href="/product"
                  className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
                >
                  Go to App
                </Link>
                <UserButton showName={true} />
              </div>
            </SignedIn>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="text-center py-16">
          <h2 className="text-6xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-6">
            Transform Your
            <br />
            Consultation Notes
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-12 max-w-2xl mx-auto">
            AI-powered assistant that generates professional summaries, action
            items, and patient communications from your consultation notes
          </p>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto mb-12">
            <div className="relative group">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-xl blur opacity-25 group-hover:opacity-40 transition duration-300"></div>
              <div className="relative bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 backdrop-blur-sm">
                <div className="text-3xl mb-4">📋</div>
                <h3 className="text-lg font-semibold mb-2 text-gray-900 dark:text-gray-100">
                  Professional Summaries
                </h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Generate comprehensive medical record summaries from your
                  notes
                </p>
              </div>
            </div>
            <div className="relative group">
              <div className="absolute inset-0 bg-gradient-to-r from-emerald-600 to-green-600 rounded-xl blur opacity-25 group-hover:opacity-40 transition duration-300"></div>
              <div className="relative bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 backdrop-blur-sm">
                <div className="text-3xl mb-4">✅</div>
                <h3 className="text-lg font-semibold mb-2 text-gray-900 dark:text-gray-100">
                  Action Items
                </h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Clear next steps and follow-up actions for every consultation
                </p>
              </div>
            </div>
            <div className="relative group">
              <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl blur opacity-25 group-hover:opacity-40 transition duration-300"></div>
              <div className="relative bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 backdrop-blur-sm">
                <div className="text-3xl mb-4">📧</div>
                <h3 className="text-lg font-semibold mb-2 text-gray-900 dark:text-gray-100">
                  Patient Emails
                </h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Draft clear, patient-friendly email communications
                  automatically
                </p>
              </div>
            </div>
          </div>

          <SignedOut>
            <SignInButton mode="modal">
              <button className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-4 px-8 rounded-xl text-lg transition-all transform hover:scale-105">
                Start Free Trial
              </button>
            </SignInButton>
          </SignedOut>
          <SignedIn>
            <Link href="/product">
              <button className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-4 px-8 rounded-xl text-lg transition-all transform hover:scale-105">
                Open Consultation Assistant
              </button>
            </Link>
          </SignedIn>
        </div>

        {/* Trust Indicators */}
        <div className="text-center text-sm text-gray-500 dark:text-gray-400">
          <p>HIPAA Compliant • Secure • Professional</p>
        </div>
      </div>
    </main>
  );
}
```

## Step 6: Update Backend Dependencies

Make sure `requirements.txt` includes Pydantic for data validation:

```
fastapi
uvicorn
openai
fastapi-clerk-auth
pydantic
```

## Step 7: Deploy Your Healthcare App

Deploy your transformed application:

```bash
vercel --prod
```

## Step 8: Test the Consultation Flow

1. Visit your production URL
2. Sign in with your account
3. Navigate to the consultation form
4. Try entering sample consultation notes:

**Example Input:**

- **Patient Name:** Jane Smith
- **Date:** Today's date
- **Notes:**
  ```
  Patient presents with persistent cough for 2 weeks. No fever.
  Chest clear on examination. Blood pressure 120/80.
  Likely viral bronchitis. Prescribed rest and fluids.
  Follow up if symptoms persist beyond another week.
  ```

You'll receive:

1. A professional summary for medical records
2. Clear next steps for the doctor
3. A patient-friendly email draft

## What's Happening?

Your healthcare app now:

- **Accepts structured input**: Form data with patient name, date, and notes
- **Validates data**: Using Pydantic models on the backend
- **Generates structured output**: Three distinct sections for different purposes
- **Maintains security**: All data is transmitted with JWT authentication
- **Supports subscriptions**: Only premium users can access the tool

## Architecture Changes from Day 3

1. **POST instead of GET**: The API now accepts form data via POST requests
2. **Structured prompts**: System and user prompts guide the AI output format
3. **Form validation**: Both frontend (required fields) and backend (Pydantic) validation
4. **Date handling**: Proper date picker with ISO format conversion
5. **Professional UI**: Healthcare-focused design with clear sections

## Security Considerations

**Important:** This is a demonstration application. For production healthcare use:

- Implement proper HIPAA compliance measures
- Add data encryption at rest and in transit
- Implement audit logging for all access
- Add role-based access control (doctor vs admin)
- Ensure proper data retention policies
- Add patient consent management

## Troubleshooting

### "Method not allowed" error

- Make sure the API endpoint uses `@app.post("/api")` not `@app.get("/api")`
- Verify the fetch request uses `method: 'POST'`

### Date picker not styled correctly

- Ensure `react-datepicker/dist/react-datepicker.css` is imported in `pages/_app.tsx`
- Check that the date picker has the correct className for Tailwind styling

### Form data not sending

- Check browser console for errors
- Verify all required fields are filled
- Ensure the JWT token is being retrieved successfully

### Output not formatting correctly

- Make sure the markdown-content styles are applied (from Day 2)
- Verify ReactMarkdown plugins are imported

## Customization Ideas

### Add More Fields

```typescript
// Add specialty selection
const [specialty, setSpecialty] = useState("General Practice");

// Add urgency level
const [urgency, setUrgency] = useState<"routine" | "urgent" | "emergency">(
  "routine"
);
```

### Enhanced Templates

Create different prompt templates for different specialties:

```python
def get_system_prompt(specialty: str) -> str:
    prompts = {
        "cardiology": "Focus on cardiac symptoms and cardiovascular health...",
        "pediatrics": "Use child-friendly language in patient communications...",
        "psychiatry": "Include mental health considerations and resources..."
    }
    return prompts.get(specialty, system_prompt)
```

### Export Options

Add buttons to export the generated content:

```typescript
const handleExportPDF = () => {
  // Generate PDF from markdown
};

const handleCopyEmail = () => {
  // Copy email section to clipboard
};
```

## Next Steps

Congratulations! You've built a professional healthcare consultation assistant with:

- ✅ Structured medical data input
- ✅ AI-powered content generation
- ✅ Professional and patient-friendly outputs
- ✅ Secure authentication and subscriptions
- ✅ Modern, accessible UI

### Potential Enhancements

1. **Template library**: Pre-built templates for common conditions
2. **Voice input**: Dictation support for notes
3. **Multi-language**: Support for patient emails in different languages
4. **Integration**: Connect with EHR systems
5. **Analytics**: Track consultation patterns and time saved
6. **Collaboration**: Allow multiple doctors to share templates

Your healthcare assistant is ready to help medical professionals save time and improve patient communication!

# Day 5: Deploy Your SaaS to AWS App Runner

## From Vercel to AWS: Professional Cloud Deployment

Today, you'll take your Healthcare Consultation Assistant from Vercel and deploy it to AWS using Docker containers and App Runner. This is how professional teams deploy production applications at scale.

## What You'll Learn

- **Docker containerization** for consistent deployments
- **AWS fundamentals** and account setup
- **AWS App Runner** for serverless container hosting
- **Production deployment** patterns used by engineering teams
- **Cost monitoring** to keep your AWS bill under control

## Important: Budget Protection First! 💰

AWS charges for resources you use. Let's set up cost alerts BEFORE deploying anything:

**Expected costs**: With our configuration, expect ~$5-10/month. AWS offers free tier credits for new accounts that should cover your first 3 months.

We'll set up budget alerts at $1, $5, and $10 to track spending. This is a crucial professional practice!

## Understanding AWS Services We'll Use

Before we start, let's understand the AWS services:

### AWS App Runner

**App Runner** is AWS's simplest way to deploy containerized web applications. Think of it as "Vercel for Docker containers" - it automatically handles HTTPS certificates, load balancing, and scaling. You just provide a container, and App Runner does the rest.

### Amazon ECR (Elastic Container Registry)

**ECR** is like GitHub but for Docker images. It's where we'll store our containerized application before deploying it to App Runner.

### AWS IAM (Identity and Access Management)

**IAM** controls who can access what in your AWS account. We'll create a special user account with limited permissions for safety - never use your root account for daily work!

### CloudWatch

**CloudWatch** is AWS's monitoring service. It collects logs from your application and helps you debug issues - like having the browser console for your server.

## Part 1: Create Your AWS Account

## WAIT - HEADS UP - DISCOVERY SINCE GOING TO PRESS!

There's an option for first time users of AWS to select the "free tier" of AWS. Don't choose this! It only has limited access to AWS services, including no access to App Runner (the service we use today). This doesn't mean that you need to pay a subscription or pay for support; just that you need to enter payment details and not be in a sandbox environment. Student Jake C. confirmed that $120 free credits still applied even after signing up for a full account.

This was discovered brilliantly by student Andy C. who shared:

> **Cryptic App Runner service error message: "The AWS Access Key Id needs a subscription for the service"**
>
> I struggled with this message for 24 hours and wanted to let everyone know the root cause. I get it when (1) I try to set up a new "Auto scaling" config (e.g., "Basic" that Ed suggests) and (2) when I try to save and create my app runner service.
>
> Here was the problem: I was signed up for the free tier of AWS. Apparently the free tier does not allow for you to use App Runner. Argh. Once I upgraded to paid tier, I was golden.
>
> I tried so many other things to try to fix this issue and spent hours trying to understand IAM, thinking that was the problem. I hope this message saves someone else a huge amount of time!

This is an example of the kind of infrastructure horrors you may face - and with enormous appreciation to Andy for digging in, finding the root cause and sharing with us all.

With that in mind:

### Step 1: Sign Up for AWS

1. Visit [aws.amazon.com](https://aws.amazon.com)
2. Click **Create an AWS Account**
3. Enter your email and choose a password
4. Select **Personal** account type (for learning)
5. Enter payment information (required, but we'll set up cost alerts)
6. Verify your phone number via SMS
7. Select **Basic Support - Free**

You now have an AWS root account. This is like having admin access - powerful but dangerous!

### Step 2: Secure Your Root Account

1. Sign in to AWS Console
2. Click your account name (top right) → **Security credentials**
3. Enable **Multi-Factor Authentication (MFA)**:
   - Click **Assign MFA device**
   - Name: `root-mfa`
   - Select **Authenticator app**
   - Scan QR code with Google Authenticator or Authy
   - Enter two consecutive codes
   - Click **Add MFA**

### Step 3: Set Up Budget Alerts (Critical!)

1. In AWS Console, search for **Billing** and click **Billing and Cost Management**
2. In the left menu, click **Budgets**
3. Click **Create budget**
4. Select **Use a template (simplified)**
5. Choose **Monthly cost budget**
6. Set up three budgets:

**Budget 1 - Early Warning ($1)**:

- Budget name: `early-warning`
- Enter budgeted amount: `1` USD
- Email recipients: Enter your email address
- Click **Create budget**

**Budget 2 - Caution ($5)**:

- Repeat steps: Create budget → Use a template → Monthly cost budget
- Budget name: `caution-budget`
- Enter budgeted amount: `5` USD
- Email recipients: Enter your email address
- Click **Create budget**

**Budget 3 - Stop Alert ($10)**:

- Repeat steps: Create budget → Use a template → Monthly cost budget
- Budget name: `stop-budget`
- Enter budgeted amount: `10` USD
- Email recipients: Enter your email address
- Click **Create budget**

AWS will automatically notify you when:

- Your actual spend reaches 85% of budget
- Your actual spend reaches 100% of budget
- Your forecasted spend is expected to reach 100%

If you hit $10, stop and review what's running!

### Step 4: Create an IAM User for Daily Work

Never use your root account for daily work. Let's create a limited user:

1. Search for **IAM** in the AWS Console
2. Click **Users** → **Create user**
3. Username: `aiengineer`
4. Check ✅ **Provide user access to the AWS Management Console**
5. Select **I want to create an IAM user**
6. Choose **Custom password** and set a strong password
7. Uncheck ⬜ **Users must create a new password at next sign-in**
8. Click **Next**

### Step 5: Create a User Group with Permissions

We'll create a reusable permission group first, then add our user to it:

1. On the permissions page, select **Add user to group**
2. Click **Create group**
3. Group name: `BroadAIEngineerAccess`
4. In the permissions policies search, find and check these policies:
   - `AWSAppRunnerFullAccess` - to deploy applications
   - `AmazonEC2ContainerRegistryFullAccess` - to store Docker images
   - `CloudWatchLogsFullAccess` - to view logs
   - `IAMUserChangePassword` - to manage own credentials
   - IMPORTANT: also `IAMFullAccess` - I don't think I mention this in the video, but it must be included or you will get errors later! Thank you Anthony W and Jake C for pointing this out.
5. Click **Create user group**
6. Back on the permissions page, select the `BroadAIEngineerAccess` group (it should be checked)
7. Click **Next** → **Create user**
8. **Important**: Click **Download .csv file** and save it securely!

It's worth keeping in mind that you might get permissions errors thoughout the course, when AWS complains that your user doesn't have permission to do something. The solution is usually to come back to this screen (as the root user) and attach another policy! This is a very common chore working with AWS...

### Step 6: Sign In as IAM User

1. Sign out from root account
2. Go to your AWS sign-in URL (in the CSV file, looks like: `https://123456789012.signin.aws.amazon.com/console`)
3. Sign in with:
   - Username: `aiengineer`
   - Password: (the one you created)

✅ **Checkpoint**: You should see "aiengineer @ Account-ID" in the top right corner

## Part 2: Install Docker Desktop

Docker lets us package our application into a container - like a shipping container for software!

### Step 1: Install Docker Desktop

1. Visit [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Download for your system:
   - **Mac**: Download for Mac (Apple Silicon or Intel)
   - **Windows**: Download for Windows (requires Windows 10/11)
3. Run the installer
4. **Windows users**: Docker Desktop will install WSL2 if needed - accept all prompts
5. Start Docker Desktop
6. You may need to restart your computer

### Step 2: Verify Docker Works

Open Terminal (Mac) or PowerShell (Windows):

```bash
docker --version
```

You should see: `Docker version 26.x.x` or similar

Test Docker:

```bash
docker run hello-world
```

You should see a message starting with "Hello from Docker!" confirming Docker is working correctly.

✅ **Checkpoint**: Docker Desktop icon should be running (whale icon in system tray/menu bar)

## Part 3: Prepare Your Application

We need to modify our Day 4 application for AWS deployment. The key change: we'll export Next.js as static files and serve everything from a single container.

### Step 1: Update Project Structure

Your project should look like this:

```
saas/
├── pages/                  # Next.js Pages Router
├── styles/                 # CSS styles
├── api/                    # FastAPI backend
├── public/                 # Static assets
├── node_modules/
├── .env.local             # Your secrets (never commit!)
├── .gitignore
├── package.json
├── requirements.txt
├── next.config.ts
└── tsconfig.json
```

### Step 2: Convert to Static Export

**Important Architecture Change**: On Vercel, our Next.js app could make server-side requests. For AWS simplicity, we'll export Next.js as static HTML/JS files and serve them from our Python backend. This means everything runs in one container!

**Note about Middleware**:
With Pages Router, we don't use middleware files. Authentication is handled entirely by Clerk's client-side components (`<Protect>`, `<SignedIn>`, etc.) which work perfectly with static exports.

Update `next.config.ts`:

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export", // This exports static HTML/JS files
  images: {
    unoptimized: true, // Required for static export
  },
};

export default nextConfig;
```

### Step 3: Update Frontend API Calls

Since we're serving everything from the same container, we need to update how the frontend calls the backend.

Update `pages/product.tsx` - find the `fetchEventSource` call and change it:

```typescript
// Old (Vercel):
await fetchEventSource('/api', {

// New (AWS):
await fetchEventSource('/api/consultation', {
```

This works because both frontend and backend will be served from the same domain!

### Step 4: Update Backend Server

Create a new file `api/server.py` (updating our FastAPI server for AWS):

```python
import os
from pathlib import Path
from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer, HTTPAuthorizationCredentials
from openai import OpenAI

app = FastAPI()

# Add CORS middleware (allows frontend to call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clerk authentication setup
clerk_config = ClerkConfig(jwks_url=os.getenv("CLERK_JWKS_URL"))
clerk_guard = ClerkHTTPBearer(clerk_config)

class Visit(BaseModel):
    patient_name: str
    date_of_visit: str
    notes: str

system_prompt = """
You are provided with notes written by a doctor from a patient's visit.
Your job is to summarize the visit for the doctor and provide an email.
Reply with exactly three sections with the headings:
### Summary of visit for the doctor's records
### Next steps for the doctor
### Draft of email to patient in patient-friendly language
"""

def user_prompt_for(visit: Visit) -> str:
    return f"""Create the summary, next steps and draft email for:
Patient Name: {visit.patient_name}
Date of Visit: {visit.date_of_visit}
Notes:
{visit.notes}"""

@app.post("/api/consultation")
def consultation_summary(
    visit: Visit,
    creds: HTTPAuthorizationCredentials = Depends(clerk_guard),
):
    user_id = creds.decoded["sub"]
    client = OpenAI()

    user_prompt = user_prompt_for(visit)
    prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    stream = client.chat.completions.create(
        model="gpt-5-nano",
        messages=prompt,
        stream=True,
    )

    def event_stream():
        for chunk in stream:
            text = chunk.choices[0].delta.content
            if text:
                lines = text.split("\n")
                for line in lines[:-1]:
                    yield f"data: {line}\n\n"
                    yield "data:  \n"
                yield f"data: {lines[-1]}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/health")
def health_check():
    """Health check endpoint for AWS App Runner"""
    return {"status": "healthy"}

# Serve static files (our Next.js export) - MUST BE LAST!
static_path = Path("static")
if static_path.exists():
    # Serve index.html for the root path
    @app.get("/")
    async def serve_root():
        return FileResponse(static_path / "index.html")

    # Mount static files for all other routes
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
```

### Step 5: Create Environment File for AWS

Create `.env` file (copy from `.env.local` but add AWS info):

```bash
# Copy your values from .env.local
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
CLERK_JWKS_URL=https://...
OPENAI_API_KEY=sk-...

# Add AWS configuration (use your chosen region from earlier) - us-east-1 or eu-west-1 etc
DEFAULT_AWS_REGION=us-east-1
AWS_ACCOUNT_ID=123456789012
```

**To find your AWS Account ID**:

1. In AWS Console, click your username (top right)
2. Copy the 12-digit Account ID

**Important**: Add `.env` to your `.gitignore` file if not already there!

## Part 4: Create Docker Configuration

Docker lets us package everything into a single container that runs anywhere.

### Step 1: Create Dockerfile

Create `Dockerfile` in your project root:

```dockerfile
# Stage 1: Build the Next.js static files
FROM node:22-alpine AS frontend-builder

WORKDIR /app

# Copy package files first (for better caching)
COPY package*.json ./
RUN npm ci

# Copy all frontend files
COPY . .

# Build argument for Clerk public key
ARG NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
ENV NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=$NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY

# Note: Docker may warn about "secrets in ARG/ENV" - this is OK!
# The NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY is meant to be public (it starts with pk_)
# It's safe to include in the build as it's designed for client-side use

# Build the Next.js app (creates 'out' directory with static files)
RUN npm run build

# Stage 2: Create the final Python container
FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI server
COPY api/server.py .

# Copy the Next.js static export from builder stage
COPY --from=frontend-builder /app/out ./static

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Expose port 8000 (FastAPI will serve everything)
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: Create .dockerignore

Create `.dockerignore` to exclude unnecessary files:

```
node_modules
.next
.env
.env.local
.git
.gitignore
README.md
.DS_Store
*.log
.vercel
dist
build
```

## Part 5: Build and Test Locally

Let's test our containerized app before deploying to AWS.

### Step 1: Load Environment Variables

**Mac/Linux** (Terminal):

```bash
export $(cat .env | grep -v '^#' | xargs)
```

**Windows** (PowerShell):

```powershell
Get-Content .env | ForEach-Object {
    if ($_ -match '^(.+?)=(.+)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
    }
}
```

### Step 2: Build the Docker Image

Build your container:

**Mac/Linux**:

```bash
docker build \
  --build-arg NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY="$NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY" \
  -t consultation-app .
```

**Windows PowerShell**:

```powershell
docker build `
  --build-arg NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY="$env:NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY" `
  -t consultation-app .
```

This will take 2-3 minutes the first time.

### Step 3: Run Locally

**Mac/Linux**:

```bash
docker run -p 8000:8000 \
  -e CLERK_SECRET_KEY="$CLERK_SECRET_KEY" \
  -e CLERK_JWKS_URL="$CLERK_JWKS_URL" \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  consultation-app
```

**Windows PowerShell**:

```powershell
docker run -p 8000:8000 `
  -e CLERK_SECRET_KEY="$env:CLERK_SECRET_KEY" `
  -e CLERK_JWKS_URL="$env:CLERK_JWKS_URL" `
  -e OPENAI_API_KEY="$env:OPENAI_API_KEY" `
  consultation-app
```

### Step 4: Test Your Application

1. Open browser to `http://localhost:8000`
2. Sign in with your Clerk account
3. Test the consultation form
4. Verify everything works!

**To stop**: Press `Ctrl+C` in the terminal

✅ **Checkpoint**: Application works identically to Vercel version

## Part 6: Deploy to AWS

Now let's deploy our container to AWS App Runner!

### Step 1: Create ECR Repository

ECR (Elastic Container Registry) is where we'll store our Docker image.

1. In AWS Console, search for **ECR**
2. Click **Get started** or **Create repository**
3. **Important**: Make sure you're in the correct region (top right of AWS Console - should match your DEFAULT_AWS_REGION)
4. Settings:
   - Visibility settings: **Private**
   - Repository name: `consultation-app` (must match exactly!)
   - Leave all other settings as default
5. Click **Create repository**
6. **Verify**: You should see your new `consultation-app` repository in the list

### Step 2: Set Up AWS CLI

We need AWS CLI to push our image.

#### Create Access Keys

1. In AWS Console, go to **IAM**
2. Click **Users** → click on `aiengineer`
3. Click **Security credentials** tab
4. Under **Access keys**, click **Create access key**
5. Select **Command Line Interface (CLI)**
6. Check the confirmation box → **Next**
7. Description: `Docker push access`
8. Click **Create access key**
9. **Critical**: Download CSV or copy both:
   - Access key ID (like: `AKIAIOSFODNN7EXAMPLE`)
   - Secret access key (like: `wJalrXUtnFEMI/K7MDENG/bPxRfiCY`)
10. Click **Done**

#### Configure AWS CLI

Install AWS CLI if you haven't:

- **Mac**: `brew install awscli` or download from [aws.amazon.com/cli](https://aws.amazon.com/cli/)
- **Windows**: Download installer from [aws.amazon.com/cli](https://aws.amazon.com/cli/)

Configure it:

```bash
aws configure
```

Enter:

- AWS Access Key ID: (paste your key)
- AWS Secret Access Key: (paste your secret)
- Default region: Choose based on your location:
  - **US East Coast**: `us-east-1` (N. Virginia)
  - **US West Coast**: `us-west-2` (Oregon)
  - **Europe**: `eu-west-1` (Ireland)
  - **Asia**: `ap-southeast-1` (Singapore)
  - **Pick the closest region for best performance!**
- Default output format: `json`

**Important**: Remember your region choice - you'll use it throughout this course!

### Step 3: Push Image to ECR

1. In ECR console, click your `consultation-app` repository
2. Click **View push commands**
3. Since you already have your AWS info in `.env`, let's use it!

**First, make sure your environment variables are loaded** (from Part 5, Step 1).

**Understanding the authentication**: The first command gets a temporary password from AWS and pipes it to Docker. You won't be prompted for a password - it's all automatic!

**Mac/Linux**:

```bash
# 1. Authenticate Docker to ECR (using your .env values!)
aws ecr get-login-password --region $DEFAULT_AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$DEFAULT_AWS_REGION.amazonaws.com

# 2. Build for Linux/AMD64 (CRITICAL for Apple Silicon Macs!)
docker build \
  --platform linux/amd64 \
  --build-arg NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY="$NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY" \
  -t consultation-app .

# 3. Tag your image (using your .env values!)
docker tag consultation-app:latest $AWS_ACCOUNT_ID.dkr.ecr.$DEFAULT_AWS_REGION.amazonaws.com/consultation-app:latest

# 4. Push to ECR
docker push $AWS_ACCOUNT_ID.dkr.ecr.$DEFAULT_AWS_REGION.amazonaws.com/consultation-app:latest
```

**Windows PowerShell**:

```powershell
# 1. Authenticate Docker to ECR (using your .env values!)
aws ecr get-login-password --region $env:DEFAULT_AWS_REGION | docker login --username AWS --password-stdin "$env:AWS_ACCOUNT_ID.dkr.ecr.$env:DEFAULT_AWS_REGION.amazonaws.com"

# 2. Build for Linux/AMD64
docker build `
  --platform linux/amd64 `
  --build-arg NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY="$env:NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY" `
  -t consultation-app .

# 3. Tag your image (using your .env values!)
docker tag consultation-app:latest "$env:AWS_ACCOUNT_ID.dkr.ecr.$env:DEFAULT_AWS_REGION.amazonaws.com/consultation-app:latest"

# 4. Push to ECR
docker push "$env:AWS_ACCOUNT_ID.dkr.ecr.$env:DEFAULT_AWS_REGION.amazonaws.com/consultation-app:latest"
```

**Note for Apple Silicon (M1/M2/M3) Macs**: The `--platform linux/amd64` flag is ESSENTIAL. Without it, your container won't run on AWS!

The push will take 2-5 minutes depending on your internet speed.

✅ **Checkpoint**: In ECR console, you should see your image with tag `latest`

## Part 7: Create App Runner Service

### Step 1: Launch App Runner

1. In AWS Console, search for **App Runner**
2. Click **Create service**

### Step 2: Configure Source

1. **Source**:
   - Repository type: **Container registry**
   - Provider: **Amazon ECR**
2. Click **Browse**
3. Select `consultation-app` → Select `latest` tag
4. **Deployment settings**:
   - Deployment trigger: **Manual** (to control costs)
   - ECR access role: **Create new service role**
5. Click **Next**

### Step 3: Configure Service

1. **Service name**: `consultation-app-service`

2. **Virtual CPU & memory**:

   - vCPU: `0.25 vCPU`
   - Memory: `0.5 GB`

3. **Environment variables** - Click **Add environment variable** for each:

   - `CLERK_SECRET_KEY` = (paste your value)
   - `CLERK_JWKS_URL` = (paste your value)
   - `OPENAI_API_KEY` = (paste your value)

   Note: We don't need `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` here - it's baked into the static files!

4. **Port**: `8000` (Important: our FastAPI server runs on 8000)

5. **Auto scaling**:

   - Minimum size: `1` (AWS requires at least 1 instance)
   - Maximum size: `1` (keeps costs low)

6. Click **Next**

### Step 4: Configure Health Check

1. **Health check configuration**:

   - Protocol: **HTTP**
   - Path: `/health`
   - Interval: `20` seconds (maximum allowed)
   - Timeout: `5` seconds
   - Healthy threshold: `2`
   - Unhealthy threshold: `5`

2. Click **Next**

### Step 5: Review and Create

1. Review all settings
2. Click **Create & deploy**
3. **Wait 5-10 minutes** - watch the Events log
4. Status will change from "Operation in progress" to "Running"

✅ **Checkpoint**: Service shows "Running" with green checkmark

### Step 6: Access Your Application

1. Click on the **Default domain** URL (like: `abc123.YOUR-REGION.awsapprunner.com`)
2. Your app should load with HTTPS automatically enabled!
3. Test all functionality:
   - Sign in with Clerk
   - Create a consultation summary
   - Sign out

🎉 **Congratulations!** Your healthcare app is now running on AWS!

## Part 8: Monitoring and Debugging

### View Logs

1. In your App Runner service, click **Logs** tab
2. **Application logs**: Your app's console output
3. **System logs**: Deployment and infrastructure logs
4. Click **View in CloudWatch** for detailed analysis

### Common Issues and Solutions

**"Unhealthy" status**:

- Check application logs for Python errors
- Verify all environment variables are set
- Ensure health check path is `/health`

**"Authentication failed"**:

- Double-check Clerk environment variables
- Verify JWKS URL is correct
- Check CloudWatch logs for specific errors

**Page not loading**:

- Ensure port is set to `8000`
- Check that Docker image was built with `--platform linux/amd64`
- Verify static files are being served

## Part 9: Updating Your Application

When you make code changes:

### Step 1: Rebuild and Push

**Mac/Linux**:

```bash
# 1. Rebuild with platform flag
docker build \
  --platform linux/amd64 \
  --build-arg NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY="$NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY" \
  -t consultation-app .

# 2. Tag for ECR (use your account ID and region from .env file)
docker tag consultation-app:latest YOUR-ACCOUNT-ID.dkr.ecr.YOUR-REGION.amazonaws.com/consultation-app:latest

# 3. Push to ECR
docker push YOUR-ACCOUNT-ID.dkr.ecr.YOUR-REGION.amazonaws.com/consultation-app:latest
```

**Windows PowerShell**:

```powershell
# 1. Rebuild with platform flag
docker build `
  --platform linux/amd64 `
  --build-arg NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY="$env:NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY" `
  -t consultation-app .

# 2. Tag for ECR (use your account ID and region from .env file)
docker tag consultation-app:latest YOUR-ACCOUNT-ID.dkr.ecr.YOUR-REGION.amazonaws.com/consultation-app:latest

# 3. Push to ECR
docker push YOUR-ACCOUNT-ID.dkr.ecr.YOUR-REGION.amazonaws.com/consultation-app:latest
```

### Step 2: Deploy Update

1. Go to App Runner console
2. Click your service
3. Click **Deploy**
4. Wait for deployment to complete

## Cost Management

### What This Costs

With our minimal configuration (1 instance always running):

- App Runner: ~$0.007/hour = ~$5/month for continuous running
- ECR: ~$0.10/GB/month for image storage
- Total: ~$5-6/month

**Note**: AWS App Runner requires at least 1 instance running, so you'll pay for continuous availability. To save money, you can pause the service when not in use.

### How to Save Money

1. **Pause when not using**: Pause your App Runner service (Actions → Pause service)
2. **Use free tier**: New AWS accounts get credits
3. **Monitor budgets**: Check your email for alerts
4. **Clean up ECR**: Delete old image versions

### Emergency Cost Control

If you hit budget alerts:

1. Go to App Runner → Select service → **Actions** → **Pause service**
2. Review CloudWatch logs for any issues
3. Check ECR for multiple image versions (delete old ones)

## What You've Accomplished

You've successfully:

- ✅ Created a production AWS account with security best practices
- ✅ Containerized a full-stack application with Docker
- ✅ Deployed to AWS App Runner with HTTPS and monitoring
- ✅ Set up cost controls and budget alerts
- ✅ Learned professional deployment patterns

## Architecture Comparison: Vercel vs AWS

**Vercel Architecture**:

- Next.js runs on Vercel's servers
- API routes handled by Vercel Functions
- Automatic deployments from Git
- Zero-config setup

**AWS Architecture**:

- Everything runs in a single Docker container
- FastAPI serves both API and static files
- Manual deployments (or automated with CI/CD)
- Full control over infrastructure

Both are valid approaches! Vercel optimizes for developer experience, while AWS offers more control and flexibility.

## Next Steps

### Immediate Improvements

1. **Custom domain**: Add your own domain in App Runner settings
2. **Auto-deployment**: Set up GitHub Actions for automated deployments
3. **Monitoring**: Add CloudWatch alarms for errors

### Advanced Enhancements

1. **Database**: Add Amazon RDS for data persistence
2. **File storage**: Use S3 for user uploads
3. **Caching**: Add ElastiCache for performance
4. **CDN**: Use CloudFront for global distribution
5. **Secrets Manager**: Store sensitive data securely

## Troubleshooting Reference

### Docker Issues

**"Cannot connect to Docker daemon"**:

```bash
# Make sure Docker Desktop is running
# Mac: Check for whale icon in menu bar
# Windows: Check system tray
```

**"Exec format error" when running container**:

```bash
# You forgot --platform flag. Rebuild:
docker build --platform linux/amd64 ...
```

### AWS Issues

**"Unauthorized" in ECR push**:

```bash
# Re-authenticate (use your region):
aws ecr get-login-password --region YOUR-REGION | docker login --username AWS --password-stdin [your-ecr-url]
```

**"Access Denied" errors**:

- Check IAM user has all required policies
- Verify AWS CLI is configured with correct credentials

### Application Issues

**Clerk authentication not working**:

- Verify all three Clerk environment variables
- Check JWKS URL matches your Clerk app
- Ensure frontend was built with public key

**API calls failing**:

- Check browser console for CORS errors
- Verify `/api/consultation` path is correct
- Check CloudWatch logs for Python errors

## Conclusion

Congratulations on deploying your healthcare SaaS to AWS! You've learned:

1. **Docker basics** - containerizing applications
2. **AWS fundamentals** - IAM, ECR, App Runner
3. **Production deployment** - security, monitoring, cost control
4. **DevOps practices** - CI/CD preparation, logging, health checks

This is how professional engineering teams deploy production applications. You now have the skills to deploy any containerized application to AWS!

## Resources

- [AWS App Runner Documentation](https://docs.aws.amazon.com/apprunner/)
- [Docker Documentation](https://docs.docker.com/)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [AWS Cost Management](https://aws.amazon.com/aws-cost-management/)

Remember to monitor your AWS costs and pause/delete resources when not in use. Happy deploying! 🚀
