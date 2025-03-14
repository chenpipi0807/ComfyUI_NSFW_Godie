import setuptools

setuptools.setup(
    name="ComfyUI_NSFW_Godie",
    version="1.0.0",
    author="Godie",
    author_email="author@example.com",
    description="A ComfyUI node for filtering NSFW text content",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ComfyUI_NSFW_Godie",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=True,
)
