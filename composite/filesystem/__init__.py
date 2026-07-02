"""A file-system tree modelled with the Composite pattern.

* :class:`~composite.filesystem.entry.Entry` — the **Component**
* :class:`~composite.filesystem.file.File` — the **Leaf**
* :class:`~composite.filesystem.directory.Directory` — the **Composite**

Client code works with ``Entry`` and never needs to know whether it is
holding a single file or a whole directory tree.
"""
