## Introduction
{. #abstract}

This Oxford Common File Layout (OCFL) specification describes an
application-independent approach to the storage of digital objects in a
structured, transparent, and predictable manner. It is designed to
promote long-term access and management of digital objects within
digital repositories.

### Need
{. #need}

The OCFL initiative began as a discussion amongst digital repository
practitioners to identify well-defined, common, and application-
independent file management for a digital repository's persisted objects
and represents a specification of the community’s collective
recommendations addressing five primary requirements: completeness,
parsability, versioning, robustness, and storage diversity.

#### Completeness
{. #completeness}

The OCFL recommends storing metadata and the content it describes
together so the OCFL object can be fully understood in the absence of
original software. The OCFL does not make recommendations about what
constitutes an object, nor does it assume what type of metadata is
needed to fully understand the object, recognizing those decisions may
differ from one repository to another. However, it is recommended that
when making this decision, implementers consider what is necessary to
rebuild the objects from the files stored.

#### Parsability
{. #parsability}

One goal of the OCFL is to ensure objects remain fixed over time. This
can be difficult as software and infrastructure change, and content is
migrated. To combat this challenge, the OCFL ensures that both humans
and machines can understand the layout and corresponding inventory
regardless of the software or infrastructure used. This allows for
humans to read the layout and corresponding inventory, and understand it
without the use of machines. Additionally, if existing software were to
become obsolete, the OCFL could easily be understood by a light weight
application, even without the full feature repository that might have
been used in the past.

#### Versioning
{. #versioning}

Another need expressed by the community was the need to update and
change objects, either the content itself or the metadata associated
with the object. The OCFL relies heavily on the prior art in the
[[Moab]] Design for Digital Object Versioning which utilizes forward
deltas to track the history of the object. Utilizing this schema allows
implementers of the OCFL to easily recreate past versions of an OCFL
object. Like with objects, the OCFL remains silent on when versioning
should occur recognizing this may differ from implementation to
implementation.

#### Robustness
{. #robustness}

The OCFL also fills the need for robustness against errors, corruption,
and migration. The versioning schema ensures an OCFL object is robust
enough to allow for the discovery of human errors. The fixity checking
built into the OCFL via content addressable storage allows implementers
to identify file corruption that might happen outside of normal human
interactions. The OCFL eases content migrations by providing a
technology agnostic method for verifying OCFL objects have remained
fixed.

#### Storage diversity
{. #storage-diversity}

Finally, the community expressed a need to store content on a wide
variety of storage technologies. With that in mind, the OCFL was written
with an eye toward various storage infrastructures including cloud
object stores.

### Note
{. #note}

This normative specification describes the nature of an OCFL Object (the
"object-at-rest") and the arrangement of OCFL Objects under an OCFL
Storage Root. A set of recommendations for how OCFL Objects should be
acted upon (the "object-in-motion") can be found in the [[OCFL-
Implementation-Notes]]. The OCFL editorial group recommends reading both
the specification and the implementation notes in order to understand
the full scope of the OCFL.

This specification is designed to operate on storage systems that employ
a hierarchical metaphor for presenting data to users. On traditional
disk-based storage this may take the form of files and directories, and
this is the terminology we use in this specification since it is widely
known. However, it may equally apply to object stores, where namespaces,
containers, and objects present a similar organization hierarchy to
users.

## Status of This Document
{. #sotd}

This document is draft of a potential specification. It has no official
standing of any kind and does not represent the support or consensus of
any standards organisation.

INSERT_TOC_HERE

## Conformance

As well as sections marked as non-normative, all authoring guidelines,
diagrams, examples, and notes in this specification are non-normative.
Everything else in this specification is normative.

The key words may, must, must not, should, and should not are to be
interpreted as described in [RFC2119].

## Terminology
{. #terminology}

DL LIST

## OCFL Object
{. #object-spec}

An OCFL Object is a group of one or more content files and
administrative information, that are together identified by a URI. The
object may contain a sequence of versions of the files that represent
the evolution of the object's contents.

A file is defined as a content bitstream that can be stored and
transmitted. Directories (also called "folders") allow for the
organization of files into tree-like hierarchies. The content of an OCFL
Object is the files and the directories they are organized in that are
stored _within_ the hierarchy layout described in this specification.

An OCFL Object includes administrative information that identifies a
directory as an OCFL Object, and also provides a means of tracking
changes to the contents of the object over time.

An OCFL Object is therefore:

1. A conceptual gathering of all files (data and metadata), the
directories they are organized in, and their changes over time which
together form the digital representation of an entity that need to be
managed, in preservation terms, as a single coherent whole (i.e.,
content); and

2. A file and directory layout and administrative information on a
storage medium that provides a defined structure for the storage of this
content, and through which these files and their changes may be
understood (i.e., structure).

A key goal of the OCFL is the rebuildability of a repository from an
OCFL Storage Root without additional information resources.
Consequently, a key implementation consideration should be to ensure
that OCFL Objects contain all the data and metadata required to achieve
this. With reference to the [[OAIS]] model, this would include all the
descriptive, administrative, structural, representation and preservation
metadata relevant to the object.

A central feature of the OCFL specification is support for versioning.
This recognizes that digital objects will change over time, through new
requirements, fixes, updates, or format shifts. The specification takes
no position on what constitutes a version or a versionable action, but
it is recommended that implementers have a clear position on this within
their local storage policies.

### Object Structure
{. #object-structure}

The OCFL Object structure organizes content files and administrative
information in order to support content storage and object validation.
The structure for an object with one version is shown in the following
figure:

```
[object_root]
    ├── 0=ocfl_object_1.1
    ├── inventory.json
    ├── inventory.json.sha512
    └── v1
        ├── inventory.json
        ├── inventory.json.sha512
        └── content
               └── ... content files ...
```

The [OCFL Object Root](#OCFL Object Root)<span id=E001>MUST NOT</span>
contain files or directories other than those specified in the following
sections.

### Object Conformance Declaration
{. #object-conformance-declaration}

The OCFL specification version declaration <span id=E002>MUST</span> be
formatted according to the [[!NAMASTE]] specification. There <span
id=E003>MUST</span> be exactly one version declaration file in the base
directory of the [OCFL Object Root](#OCFL Object Root) giving the OCFL
version in the filename. The filename <span id=E004>MUST</span> conform
to the pattern `T=dvalue`, where `T`<span id=E005>MUST</span> be 0, and
`dvalue`<span id=E006>MUST</span> be `ocfl_object_`, followed by the
OCFL specification version number. The text contents of the file <span
id=E007>MUST</span> be the same as `dvalue`, followed by a newline
(`\n`).

### Version Directories
{. #version-directories}

OCFL Object content <span id=E008>MUST</span> be stored as a sequence of
one or more versions. Each object version is stored in a version
directory under the object root. Version directory names <span
id=E104>MUST</span> be constructed by prepending `v` to the version
number. The version number <span id=E105>MUST</span> be taken from the
sequence of positive, base-ten integers: 1, 2, 3, etc.. The version
number sequence <span id=E009>MUST</span> start at 1 and <span
id=E010>MUST</span> be continuous without missing integers.

Implementations <span id=W001>SHOULD</span> use version directory names
constructed without zero-padding the version number, ie. `v1`, `v2`,
`v3`, etc..

For compatibility with existing filesystem conventions, implementations
MAY use zero-padded version directory numbers, with the following
restriction: If zero-padded version directory numbers are used then they
<span id=E011>MUST</span> start with the prefix `v` and then a zero. For
example, in an implementation that uses five digits for version
directory names then `v00001` to `v09999` are allowed, `v10000` is not
allowed.

The first version of an object defines the naming convention for all
version directories for the object. All version directories of an object
<span id=E012>MUST</span> use the same naming convention: either a non-
padded version directory number, or a zero-padded version directory
number of consistent length. The version naming convention <span
id=E013>MUST</span> be consistent across all versions. In all cases,
references to files inside version directories from inventory files
<span id=E014>MUST</span> use the actual version directory names.

There <span id=E015>MUST</span> be no other files as children of a
version directory, other than an [inventory file](#inventory) and a
[inventory digest](#inventory-digest). The version directory <span
id=W002>SHOULD NOT</span> contain any directories other than the
designated content sub-directory. Once created, the contents of a
version directory are expected to be immutable.

#### Content Directory
{. #content-directory}

Version directories <span id=E016>MUST</span> contain a designated
content sub-directory if the version contains files to be preserved, and
<span id=W003>SHOULD NOT</span> contain this sub-directory otherwise.
The name of this designated sub-directory MAY be defined in the
[inventory file](#inventory) using the key `contentDirectory` with the
value being the chosen sub-directory name as a string, relative to the
version directory. The `contentDirectory` value <span
id=E0108>MUST</span> represent a direct child directory of the version
directory in which it is found. As such, the `contentDirectory` value
<span id=E017>MUST NOT</span> contain the forward slash (`/`) path
separator and <span id=E018>MUST NOT</span> be either one or two periods
(`.` or `..`). If the key `contentDirectory` is set, it <span
id=E019>MUST</span> be set in the first version of the object and <span
id=E020>MUST NOT</span> change between versions of the same object.

If the key `contentDirectory` is not present in the [inventory
file](#inventory) then the name of the designated content sub-directory
<span id=E021>MUST</span> be `content`. OCFL-compliant tools (including
any validators) <span id=E022>MUST</span> ignore all directories in the
object version directory except for the designated content directory.

Every file within a version's content directory <span
id=E023>MUST</span> be referenced in the [manifest](#manifest) section
of that version's inventory. There <span id=E024>MUST NOT</span> be
empty directories within a version's content directory. A directory that
would otherwise be empty MAY be maintained by creating a file within it
named according to local conventions, for example by making an empty
`.keep` file.

### Digests
{. #digests}

A [digest](#digest) plays two roles in an OCFL Object. The first is that
digests allow for content-addressable reference to files within the OCFL
Object. That is, the connection between a file's [content path](#content
path) on physical storage and its [logical path](#logical path) in a
version of the object's content is made with a digest of its contents,
rather than its filename. This use of the content digest facilitates de-
duplication of files with the same content within an object, such as
files that are unchanged from one version to the next. The second role
that digests play is provide for fixity checks to determine whether a
file has become corrupt, through hardware degradation or accident for
example.

For content-addressing, OCFL Objects <span id=E025>MUST</span> use
either `sha512` or `sha256`, and <span id=W004>SHOULD</span> use
`sha512`. The choice of the `sha512` digest algorithm as default
recognizes that it has no known collision vulnerabilities and multiple
implementations are available.

For storage of additional fixity values, or to support legacy content
migration, implementers <span id=E026>MUST</span> choose from the
following controlled vocabulary of digest algorithms, or from a list of
additional algorithms given in the [[Digest-Algorithms-Extension]]. OCFL
clients <span id=E027>MUST</span> support all fixity algorithms given in
the table below, and MAY support additional algorithms from the
extensions. Optional fixity algorithms that are not supported by a
client <span id=E028>MUST</span> be ignored by that client.

TABLE

An OCFL Inventory MAY contain a fixity section that can store one or
more blocks containing fixity values using multiple digest algorithms.
See the [section on fixity](#fixity) below for further details.

> Non-normative note: Implementers may also store copies of their file
digests in a system external to their OCFL Object stores at the point of
ingest, to further safeguard against the possibility of malicious
manipulation of file contents and digests.

> Implementers should be aware that base16 digests are case insensitive.
Different tools will generate digests in uppercase or lowercase, and
this may lead to case differences between references to a digest and the
digest itself within the inventory. If string-based methods are used to
work with digests and inventories (as is the case in most common JSON
libraries) then extra care must be taken to ensure case-insensitive
comparisons are being made.

### Inventory
{. #inventory}

An OCFL Object Inventory <span id=E033>MUST</span> follow the JSON
(defined by [[!RFC8259]]) structure described in this section with
contents encoded in UTF-8, and <span id=E034>MUST</span> be named
`inventory.json`. The order of entries in both the JSON objects and
arrays used in inventory files has no significance. An OCFL Object
Inventory <span id=E102>MUST NOT</span> contain any keys not described
in this specification.

The forward slash (/) path separator <span id=E035>MUST</span> be used
in content paths in the [manifest](#manifest) and [fixity](#fixity)
blocks within the inventory. Implementations that target systems using
other separators will need to translate paths appropriately.

> Non-normative note: A [[JSON-Schema]] for validating OCFL Object
Inventory files is provided at
[inventory_schema.json](inventory_schema.json).

#### Basic Structure
{. #inventory-structure}

Every OCFL inventory <span id=E036>MUST</span> include the following
keys:

DL LIST

There MAY be the following key:

DL LIST

In addition to these keys, there <span id=E041>MUST</span> be two other
blocks present, `manifest` and `versions`, which are discussed in the
next two sections.

#### Manifest
{. #manifest}

The value of the `manifest` key <span id=E106>MUST</span> be a JSON
object, and each key <span id=E107>MUST</span> correspond to a digest
value key found in one or more `state` blocks of the current and/or
previous `version` blocks of the [OCFL Object](#OCFL Object). The value
for each key <span id=E092>MUST</span> be an array containing the
[content path](#content path)s of files in the OCFL Object that have
content with the given digest. As JSON keys are case sensitive, for
digest algorithms with case insensitive digest values, there is an
additional requirement that each digest value <span id=E096>MUST</span>
occur only once in the manifest block for any digest algorithm,
regardless of case. Content paths within a manifest block <span
id=E042>MUST</span> be relative to the [OCFL Object Root](#OCFL Object
Root). The following restrictions avoid ambiguity and provide path
safety for clients processing the `manifest`.

* The content path <span id=E098>MUST</span> be interpreted as a set of
one or more path elements joined by a `/` path separator.

* Path elements <span id=E099>MUST NOT</span> be `.`, `..`, or empty
(`//`).

* A content path <span id=E100>MUST NOT</span> begin or end with a
forward slash (`/`).

* Within an inventory, content paths <span id=E101>MUST</span> be unique
and non-conflicting, so the content path for a file cannot appear as the
initial part of another content path.

> Non-normative note: If only one file is stored in the OCFL Object for
each digest, fully de-duplicating the content, then there will be only
one [content path](#content path) for each digest. There may, however,
be multiple logical paths for a given digest if the content was not
entirely de-duplicated when constructing the OCFL Object.

> An example manifest object for three content paths, all in version 1,
is shown below:

```
> 
  "manifest": {
    "7dcc35...c31": [ "v1/content/foo/bar.xml" ],
    "cf83e1...a3e": [ "v1/content/empty.txt" ],
    "ffccf6...62e": [ "v1/content/image.tiff" ]
  }
```

#### Versions
{. #versions}

An OCFL Object Inventory <span id=E043>MUST</span> include a block for
storing versions. This block <span id=E044>MUST</span> have the key of
`versions` within the inventory, and it <span id=E045>MUST</span> be a
JSON object. The keys of this object <span id=E046>MUST</span>
correspond to the names of the [version directories](#version-
directories) used. Each value <span id=E047>MUST</span> be another JSON
object that characterizes the version, as described in the
[FIXME](#version) section.

##### Version
{. #version}

A JSON object to describe one [OCFL Version](#OCFL Version), which <span
id=E048>MUST</span> include the following keys:

DL LIST

The JSON object describing an [OCFL Version](#OCFL Version), <span
id=W007>SHOULD</span> include the following keys:

DL LIST

#### Fixity
{. #fixity}

An OCFL Object inventory MAY include a block for storing additional
fixity information to supplement the complete set of digests in the
[Manifest](#manifest), for example to support legacy digests from a
content migration. If present, this block <span id=E055>MUST</span> have
the key of `fixity` within the inventory, and its value <span
id=E111>MUST</span> be a JSON object, which MAY be empty.

The keys within the `fixity` block <span id=E056>MUST</span> correspond
to the controlled vocabulary of [digest algorithm names](#digest-
algorithms) listed in the [Digests](#digests) section, or in a table
given in an [Extension](#Extension). The value of the fixity block for a
particular digest algorithm <span id=E057>MUST</span> follow the
structure of the [FIXME](#manifest) block; that is, a key corresponding
to the digest value, and an array of [content path](#content path)s. The
`fixity` block for any digest algorithm MAY include digest values for
any subset of content paths in the object. Where included, the digest
values given <span id=E093>MUST</span> match the digests of the files at
the corresponding content paths. As JSON keys are case sensitive, for
digest algorithms with case insensitive digest values, there is an
additional requirement that each digest value <span id=E097>MUST</span>
occur only once in the `fixity` block for any digest algorithm,
regardless of case. There is no requirement that all content files have
a value in the `fixity` block, or that fixity values provided in one
version are carried forward to later versions.

> An example `fixity` with `md5` and `sha1` digests is shown below. In
this case the `md5` digest values are provided only for version 1
content paths.

```
> 
  "fixity": {
    "md5": {
      "184f84e28cbe75e050e9c25ea7f2e939": [ "v1/content/foo/bar.xml" ],
      "c289c8ccd4bab6e385f5afdd89b5bda2": [ "v1/content/image.tiff" ],
      "d41d8cd98f00b204e9800998ecf8427e": [ "v1/content/empty.txt" ]
    },
    "sha1": {
      "66709b068a2faead97113559db78ccd44712cbf2": [ "v1/content/foo/bar.xml" ],
      "a6357c99ecc5752931e133227581e914968f3b9c": [ "v2/content/foo/bar.xml" ],
      "b9c7ccc6154974288132b63c15db8d2750716b49": [ "v1/content/image.tiff" ],
      "da39a3ee5e6b4b0d3255bfef95601890afd80709": [ "v1/content/empty.txt" ]
    }
  }
```

### Inventory Digest
{. #inventory-digest}

Every occurrence of an inventory file <span id=E058>MUST</span> have an
accompanying sidecar file named `inventory.json.ALGORITHM` stating its
digest, where `ALGORITHM` is the chosen digest algorithm for the object.
The ALGORITHM <span id=E059>MUST</span> match the value given for the
`digestAlgorithm` key in the inventory. An example might be
`inventory.json.sha512`.

The digest sidecar file <span id=E060>MUST</span> contain the digest of
the inventory file. This <span id=E061>MUST</span> follow the format:

```
DIGEST inventory.json
```

One or more whitespace characters (spaces or tabs) must separate DIGEST
from the string `inventory.json`; that is, the name of the inventory
file in the same directory.

The digest of the inventory <span id=E062>MUST</span> be computed only
after all changes to the inventory have been made, and thus writing the
digest sidecar file is the last step in the versioning process.

### Version Inventory and Inventory Digest
{. #version-inventory}

Every OCFL Object <span id=E063>MUST</span> have an inventory file
within the OCFL Object Root, corresponding to the state of the OCFL
Object at the current version. Additionally, every version directory
<span id=W010>SHOULD</span> include an inventory file that is an
[Inventory](#inventory) of all content for versions up to and including
that particular version. Where an OCFL Object contains `inventory.json`
in version directories, the inventory file in the OCFL Object Root <span
id=E064>MUST</span> be the same as the file in the most recent version.
See also requirements for the corresponding [Inventory
Digest](#inventory-digest).

In the case that prior version directories include an inventory file
there will be multiple inventory files describing prior versions within
the OCFL Object. Each `version` block in each prior inventory file <span
id=E066>MUST</span> represent the same [logical state](#logical state)
as the corresponding `version` block in the current inventory file.
Additionally, the values of the `created`, `message` and `user` keys in
each `version` block in each prior inventory file <span
id=W011>SHOULD</span> have the same values as the corresponding keys in
the corresponding `version` block in the current inventory file.

#### Conformance of prior versions
{. #conformance-of-prior-versions}

Version directories in OCFL are intended to be immutable in that
existing version directories do not change when a new version directory
is added. Each version directory within an OCFL Object <span
id=E103>MUST</span> conform to either the same or a later OCFL
specification version as the preceding version directory. If inventories
are stored in the version directories then the OCFL specification
version for a given version directory is apparent from the `type`
attribute in that [inventory](#inventory-structure).

### Logs Directory
{. #logs-directory}

The base directory of an OCFL Object MAY contain a directory named
`logs`, which MAY be empty. Implementers <span id=W012>SHOULD</span> use
the [logs directory](#logs directory) for storing files that contain a
record of actions taken on the object. Since these logs may be subject
to local standards requirements, the format of these logs is considered
out-of-scope for the OCFL Object. Clients operating on the object MAY
log actions here that are not otherwise captured.

> Non-normative note: The purpose of the logs directory is to provide
implementers with a location for storing local information about actions
to the OCFL Object's content that is not part of the content itself.

> As an example, implementers may have different local requirements to
store audit information for their content. Some may wish to store a log
entry indicating that an audit was conducted, and nothing was wrong,
while others may wish to only store a log entry if an intervention was
required.

### Object Extensions
{. #object-extensions}

The base directory of an OCFL Object MAY contain a directory named
`extensions` for the purposes of extending the functionality of an OCFL
Object. The `extensions` directory <span id=E067>MUST NOT</span> contain
any files, and no sub-directories other than extension sub-directories.
Extension sub-directories <span id=W013>SHOULD</span> be named according
to a [registered extension name](#registered extension name) in the
[OCFL Extensions repository](https://ocfl.github.io/extensions/).

> Non-normative note: Extension sub-directories should use the same name
as a registered extension in order to both avoid the possiblity of an
extension sub-directory colliding with the name of another registered
extension as well as to facilitate the recognition of extensions by OCFL
clients. See also [Documenting Local Extensions](#documenting-local-
extensions).

## OCFL Storage Root
{. #storage-root}

An [OCFL Storage Root](#OCFL Storage Root) is the base directory of an
OCFL storage layout.

### Root Structure
{. #root-structure}

An OCFL Storage Root <span id=E069>MUST</span> contain a [Root
Conformance Declaration](#root-conformance-declaration) identifying it
as such.

An OCFL Storage Root MAY contain other files as direct children. These
might include a human-readable copy of the OCFL specification to make
the storage root self-documenting, or files used to [document local
extensions](#documenting-local-extensions). An OCFL validator <span
id=E087>MUST</span> ignore any files in the storage root it does not
understand.

An OCFL Storage Root <span id=E088>MUST NOT</span> contain directories
or sub-directories other than as a directory hierarchy used to store
OCFL Objects or for [storage root extensions](#storage-root-extensions).
The directory hierarchy used to store OCFL Objects <span id=E072>MUST
NOT</span> contain files that are not part of an OCFL Object. Empty
directories <span id=E073>MUST NOT</span> appear under a storage root.

An OCFL Storage Root MAY contain a file named `ocfl_layout.json` to
describe the arrangement of directories and OCFL objects under the
storage root. If present, `ocfl_layout.json`<span id=E070>MUST</span> be
a JSON (defined by [[!RFC8259]]) document encoded in UTF-8 and include
the following two keys in the root JSON object:

* `extension` - An extension name that identifies an arrangement of
directories and OCFL objects under the storage root, i.e. how OCFL
object identifiers are mapped to directory hierarchies. The value of the
`extension` key <span id=E071>MUST</span> be the [registered extension
name](#registered extension name) for the extension defining the
arrangement under the storage root.

* `description` - A human readable description of the arrangement of
directories and OCFL objects under the storage root.

Although implementations may require multiple OCFL Storage Roots—that
is, several logical or physical volumes, or multiple "buckets" in an
object store—each OCFL Storage Root <span id=E074>MUST</span> be
independent.

The following example OCFL Storage Root represents the minimal set of
files and folders:

```
[storage_root]
    ├── 0=ocfl_1.1
    ├── ocfl_1.1.txt (human-readable text of the OCFL specification; optional)
    └── ocfl_layout.json (description of storage hierarchy layout; optional)
```

### Root Conformance Declaration
{. #root-conformance-declaration}

The OCFL version declaration <span id=E075>MUST</span> be formatted
according to the [[!NAMASTE]] specification. There <span
id=E076>MUST</span> be exactly one version declaration file in the base
directory of the [OCFL Storage Root](#OCFL Storage Root) giving the OCFL
version in the filename. The filename <span id=E077>MUST</span> conform
to the pattern `T=dvalue`, where `T`<span id=E078>MUST</span> be 0, and
`dvalue`<span id=E079>MUST</span> be `ocfl_`, followed by the OCFL
specification version number. The text contents of the file <span
id=E080>MUST</span> be the same as `dvalue`, followed by a newline
(`\n`).

Root conformance indicates that the OCFL Storage Root conforms to this
section (i.e. the OCFL Storage Root section) of the specification. OCFL
Objects within the OCFL Storage Root also include a conformance
declaration which <span id=E081>MUST</span> indicate OCFL Object
conformance to the same or earlier version of the specification.

### Storage Hierarchies
{. #root-hierarchies}

[OCFL Object Root](#OCFL Object Root)s <span id=E082>MUST</span> be
stored either as the terminal resource at the end of a directory storage
hierarchy or as direct children of a containing [OCFL Storage
Root](#OCFL Storage Root).

A common practice is to use a unique identifier scheme to compose this
storage hierarchy, typically arranged according to some form of the
[[PairTree]] specification. Irrespective of the pattern chosen for the
storage hierarchies, the following restrictions apply:

1. There <span id=E083>MUST</span> be a deterministic mapping from an
object identifier to a unique storage path

2. Storage hierarchies <span id=E084>MUST NOT</span> include files
within intermediate directories

3. Storage hierarchies <span id=E085>MUST</span> be terminated by OCFL
Object Roots

4. Storage hierarchies within the same OCFL Storage Root <span
id=W014>SHOULD</span> use just one layout pattern

5. Storage hierarchies within the same OCFL Storage Root <span
id=W015>SHOULD</span> consistently use either a directory hierarchy of
OCFL Objects or top-level OCFL Objects

### Storage Root Extensions
{. #storage-root-extensions}

The behavior of the storage root may be extended to support features
from other specifications.

The base directory of an OCFL Storage Root MAY contain a directory named
`extensions` for the purposes of extending the functionality of an OCFL
Storage Root. The storage root `extensions` directory <span
id=E086>MUST</span> conform to the same guidelines and limitations as
those defined for [object extensions](#object-extensions).

> Non-normative note: Storage extensions can be used to support
additional features, such as providing the storage hierarchy disposition
when pairtree is in use, or additional human-readable text about the
nature of the storage root.

### Documenting Local Extensions
{. #documenting-local-extensions}

It is preferable that both [Object Extensions](#object-extensions) and
[Storage Root Extenstions](#storage-root-extensions) are documented and
registered in the [OCFL Extensions
repository](https://ocfl.github.io/extensions/). However, local
extensions MAY be documented by including a plain text document directly
in the storage root, thus making the storage root self-documenting.

### Filesystem features
{. #filesystem-features}

In order to maximize the compatibility of the OCFL with different
filesystems, and thus improve the portability of OCFL Objects between
different systems, some restrictions on the use of certain filesystem
features are necessary. If the preservation of non-OCFL-compliant
features is required then the content <span id=E089>MUST</span> be
wrapped in a suitable disk or filesystem image format which OCFL can
treat as a regular file.

1. Filesystem metadata (e.g. permissions, access, and creation times)
are not considered portable between filesystems or preservable through
file transfer operations. These attributes also cannot be validated in
terms of fixity in a consistent manner. As such, the OCFL does not
support the portability of these attributes.

2. Hard and soft (symbolic) links are not portable and <span
id=E090>MUST NOT</span> be used within OCFL Storage hierachies. A common
use case for links is storage deduplication. OCFL inventories provide a
portable method of achieving the same effect by using digests to address
content.

3. File paths and filenames in the OCFL are case sensitive. Filesystems
<span id=E091>MUST</span> preserve the case of OCFL filepaths and
filenames.

4. Transparent filesystem features such as compression and encryption
should be effectively invisible to OCFL operations. Consequently, they
should not be expected to be portable.

## Examples
{. #examples}

### Minimal OCFL Object
{. #example-minimal-object}

The following example OCFL Object has content that is a single file
(`file.txt`), and just one version (`v1`):

```
[object root]
    ├── 0=ocfl_object_1.1
    ├── inventory.json
    ├── inventory.json.sha512
    └── v1
        ├── inventory.json
        ├── inventory.json.sha512
        └── content
            └── file.txt
```

The inventory for this OCFL Object, the same both at the top-level and
in the `v1` directory, might be:

```
{
  "digestAlgorithm": "sha512",
  "head": "v1",
  "id": "http://example.org/minimal",
  "manifest": {
    "7545b8...f67": [ "v1/content/file.txt" ]
  },
  "type": "https://ocfl.io/1.1/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2018-10-02T12:00:00Z",
      "message": "One file",
      "state": {
        "7545b8...f67": [ "file.txt" ]
      },
      "user": {
        "address": "mailto:alice@example.org",
        "name": "Alice"
      }
    }
  }
}
```

### Versioned OCFL Object
{. #example-versioned-object}

The following example OCFL Object has three versions:

```
[object root]
    ├── 0=ocfl_object_1.1
    ├── inventory.json
    ├── inventory.json.sha512
    ├── v1
    │   ├── inventory.json
    │   ├── inventory.json.sha512
    │   └── content
    │       ├── empty.txt
    │       ├── foo
    │       │   └── bar.xml
    │       └── image.tiff
    ├── v2
    │   ├── inventory.json
    │   ├── inventory.json.sha512
    │   └── content
    │       └── foo
    │           └── bar.xml
    └── v3
        ├── inventory.json
        └── inventory.json.sha512
```

In `v1` there are three files, `empty.txt`, `foo/bar.xml`, and
`image.tiff`. In `v2` the content of `foo/bar.xml` is changed,
`empty2.txt` is added with the same content as `empty.txt`, and
`image.tiff` is removed. In `v3` the file `empty.txt` is removed, and
`image.tiff` is reinstated. As a result of forward-delta versioning, the
object tree above shows only new content added in each version. The
inventory shown below details the other changes, includes additional
fixity information using `md5` and `sha1` digest algorithms, and minimal
metadata for each version.

```
{
  "digestAlgorithm": "sha512",
  "fixity": {
    "md5": {
      "184f84e28cbe75e050e9c25ea7f2e939": [ "v1/content/foo/bar.xml" ],
      "2673a7b11a70bc7ff960ad8127b4adeb": [ "v2/content/foo/bar.xml" ],
      "c289c8ccd4bab6e385f5afdd89b5bda2": [ "v1/content/image.tiff" ],
      "d41d8cd98f00b204e9800998ecf8427e": [ "v1/content/empty.txt" ]
    },
    "sha1": {
      "66709b068a2faead97113559db78ccd44712cbf2": [ "v1/content/foo/bar.xml" ],
      "a6357c99ecc5752931e133227581e914968f3b9c": [ "v2/content/foo/bar.xml" ],
      "b9c7ccc6154974288132b63c15db8d2750716b49": [ "v1/content/image.tiff" ],
      "da39a3ee5e6b4b0d3255bfef95601890afd80709": [ "v1/content/empty.txt" ]
    }
  },
  "head": "v3",
  "id": "ark:/12345/bcd987",
  "manifest": {
    "4d27c8...b53": [ "v2/content/foo/bar.xml" ],
    "7dcc35...c31": [ "v1/content/foo/bar.xml" ],
    "cf83e1...a3e": [ "v1/content/empty.txt" ],
    "ffccf6...62e": [ "v1/content/image.tiff" ]
  },
  "type": "https://ocfl.io/1.1/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2018-01-01T01:01:01Z",
      "message": "Initial import",
      "state": {
        "7dcc35...c31": [ "foo/bar.xml" ],
        "cf83e1...a3e": [ "empty.txt" ],
        "ffccf6...62e": [ "image.tiff" ]
      },
      "user": {
        "address": "mailto:alice@example.com",
        "name": "Alice"
      }
    },
    "v2": {
      "created": "2018-02-02T02:02:02Z",
      "message": "Fix bar.xml, remove image.tiff, add empty2.txt",
      "state": {
        "4d27c8...b53": [ "foo/bar.xml" ],
        "cf83e1...a3e": [ "empty.txt", "empty2.txt" ]
      },
      "user": {
        "address": "mailto:bob@example.com",
        "name": "Bob"
      }
    },
    "v3": {
      "created": "2018-03-03T03:03:03Z",
      "message": "Reinstate image.tiff, delete empty.txt",
      "state": {
        "4d27c8...b53": [ "foo/bar.xml" ],
        "cf83e1...a3e": [ "empty2.txt" ],
        "ffccf6...62e": [ "image.tiff" ]
      },
      "user": {
        "address": "mailto:cecilia@example.com",
        "name": "Cecilia"
      }
    }
  }
}
```

### Different Logical and Content Paths in an OCFL Object
{. #example-object-diff-paths}

The following example OCFL Object inventory shows how content paths may
differ from logical paths. The example object has just one version,
`v1`, which has two files with logical paths `a file.wxy` and `another
file.xyz` as shown in the `state` block. The corresponding content paths
are `v1/content/3bacb119a98a15c5` and `v1/content/9f2bab8ef869947d`
respectively, as shown in the `manifest`. Except for location within the
appropriate version directory, `v1/content` in this example, the OCFL
specification does not constrain the choice of content paths used when
creating or updating an OCFL object. The choice might depend on
particular limitations of, or optimizations for, the target storage
system, or on portability considerations. Any compliant implementation
will be able to recover version state with the original logical paths.

```
{
  "digestAlgorithm": "sha512",
  "head": "v1",
  "id": "http://example.org/diff-paths",
  "manifest": {
    "7545b8...f67": [ "v1/content/3bacb119a98a15c5" ],
    "af318d...3cd": [ "v1/content/9f2bab8ef869947d" ]
  },
  "type": "https://ocfl.io/1.1/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2019-03-14T20:31:00Z",
      "state": {
        "7545b8...f67": [ "a file.wxy" ],
        "af318d...3cd": [ "another file.xyz" ]
      },
      "user": {
        "address": "mailto:admin@example.org",
        "name": "Some Admin"
      }
    }
  }
}
```

### BagIt in an OCFL Object
{. #example-bagit-in-ocfl}

[[BagIt]] is a common file packaging specification, but unlike the OCFL
it does not provide a mechanism for content versioning. Using the OCFL
it is possible to store a BagIt structure with content versioning, such
that when the [logical state](#logical state) is resolved, it creates a
valid BagIt 'bag'. This example will illustrate one way this can be
accomplished, using the [example of a basic
bag](https://datatracker.ietf.org/doc/html/rfc8493#section-4.1) given in
the BagIt specification.

```
[object root]
    ├── 0=ocfl_object_1.1
    ├── inventory.json
    ├── inventory.json.sha512
    └── v1
        ├── inventory.json
        ├── inventory.json.sha512
        └── content
            └── myfirstbag
                ├── bagit.txt
                ├── data
                │   └── 27613-h
                │       └── images
                │           ├── q172.png
                │           └── q172.txt
                └── manifest-md5.txt
```

If, for example, a new directory were added in a subsequent version, the
OCFL Object would look like this:

```
[object root]
    ├── 0=ocfl_object_1.1
    ├── inventory.json
    ├── inventory.json.sha512
    ├── v1
    │   ├── inventory.json
    │   ├── inventory.json.sha512
    │   └── content
    │       └── myfirstbag
    │           ├── bagit.txt
    │           ├── data
    │           │   └── 27613-h
    │           │       └── images
    │           │           ├── q172.png
    │           │           └── q172.txt
    │           └── manifest-md5.txt
    └── v2
        ├── inventory.json
        ├── inventory.json.sha512
        └── content
            └── myfirstbag
                ├── data
                │   └── 27614-h
                │       └── images
                │           ├── q173.png
                │           └── q173.txt
                └── manifest-md5.txt
```

The state of the object at version 2 would be the following BagIt
object:

```
myfirstbag
    ├── bagit.txt
    ├── data
    │   ├── 27613-h
    │   │   └── images
    │   │       ├── q172.png
    │   │       └── q172.txt
    │   └── 27614-h
    │       └── images
    │           ├── q173.png
    │           └── q173.txt
    └── manifest-md5.txt
```

The OCFL Inventory for this object would be as follows:

```
{
  "digestAlgorithm": "sha512",
  "head": "v2",
  "id": "urn:uri:example.com/myfirstbag",
  "manifest": {
    "cf83e1...a3e": [ "v1/content/myfirstbag/bagit.txt" ],
    "f15428...83f": [ "v1/content/myfirstbag/manifest-md5.txt" ],
    "85f2b0...007": [ "v1/content/myfirstbag/data/27613-h/images/q172.png" ],
    "d66d80...8bd": [ "v1/content/myfirstbag/data/27613-h/images/q172.txt" ],
    "2b0ff8...620": [ "v2/content/myfirstbag/manifest-md5.txt" ],
    "921d36...877": [ "v2/content/myfirstbag/data/27614-h/images/q173.png" ],
    "b8bdf1...927": [ "v2/content/myfirstbag/data/27614-h/images/q173.txt" ]
  },
  "type": "https://ocfl.io/1.1/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2018-10-09T11:20:29.209164Z",
      "message": "Initial Ingest",
      "state": {
        "cf83e1...a3e": [ "myfirstbag/bagit.txt" ],
        "85f2b0...007": [ "myfirstbag/data/27613-h/images/q172.png" ],
        "d66d80...8bd": [ "myfirstbag/data/27613-h/images/q172.txt" ],
        "f15428...83f": [ "myfirstbag/manifest-md5.txt" ]
      },
      "user": {
        "address": "mailto:someone@example.org",
        "name": "Some One"
      }
    },
    "v2": {
      "created": "2018-10-31T11:20:29.209164Z",
      "message": "Added new images",
      "state": {
        "cf83e1...a3e": [ "myfirstbag/bagit.txt" ],
        "85f2b0...007": [ "myfirstbag/data/27613-h/images/q172.png" ],
        "d66d80...8bd": [ "myfirstbag/data/27613-h/images/q172.txt" ],
        "2b0ff8...620": [ "myfirstbag/manifest-md5.txt" ],
        "921d36...877": [ "myfirstbag/data/27614-h/images/q173.png" ],
        "b8bdf1...927": [ "myfirstbag/data/27614-h/images/q173.txt" ]
      },
      "user": {
        "address": "mailto:somebody-else@example.org",
        "name": "Somebody Else"
      }
    }
  }
}
```

### Moab in an OCFL Object
{. #example-moab-in-ocfl}

[[Moab]] is an archive information package format developed and used by
Stanford University. Many of the ideas in Moab have been refined by the
OCFL, and the OCFL is designed to give institutions currently using Moab
an easy path to adoption.

Converting content preserved in a Moab object in a way that does not
compromise existing Moab access patterns whilst allowing for the
eventual use of OCFL-native workflows requires a Moab to OCFL conversion
tool. This tool uses the Moab-versioning gem to extract deltas and
digests of the Moab data directory for each Moab version and translate
those into version `state` blocks in an OCFL inventory file, which would
be placed in the root directory of the Moab object. The content of the
`data` directory in the Moab version directories (and thus, the
bitstreams that Moab is preserving) is tracked by OCFL, via the
`contentDirectory` value. The contents of the Moab `manifests`
directories are not tracked, as the intention is not to encapsulate a
Moab object inside an OCFL object, but rather to migrate Moab's
preserved bitstreams into an OCFL object without compromising legacy
access patterns.

During the transitionary period the OCFL inventory file exists only in
the root of the Moab object. Once OCFL-native object creation workflows
have been completed, future versions of that object will be fully OCFL
compliant - new versions will no longer have a manifests directory and
will contain an OCFL inventory file. At this stage OCFL tools will be
able to access all versions of the content originally preserved by Moab.

Consider the following sample Moab object:

```
[object root]
    └── bj102hs9687
        ├── v0001
        │     ├── data
        │     │   ├── content
        │     │   │   ├── eric-smith-dissertation-augmented.pdf
        │     │   │   └── eric-smith-dissertation.pdf
        │     │   └── metadata
        │     │       ├── contentMetadata.xml
        │     │       ├── descMetadata.xml
        │     │       ├── identityMetadata.xml
        │     │       ├── provenanceMetadata.xml
        │     │       ├── relationshipMetadata.xml
        │     │       ├── rightsMetadata.xml
        │     │       ├── technicalMetadata.xml
        │     │       └── versionMetadata.xml
        │     └── manifests
        │         ├── fileInventoryDifference.xml
        │         ├── manifestInventory.xml
        │         ├── signatureCatalog.xml
        │         ├── versionAdditions.xml
        │         └── versionInventory.xml
        ├── v0002
        │     ├── data
        │     │   └── metadata
        │     │       ├── contentMetadata.xml
        │     │       ├── embargoMetadata.xml
        │     │       ├── events.xml
        │     │       ├── identityMetadata.xml
        │     │       ├── provenanceMetadata.xml
        │     │       ├── relationshipMetadata.xml
        │     │       ├── rightsMetadata.xml
        │     │       ├── versionMetadata.xml
        │     │       └── workflows.xml
        │     └── manifests
        │         ├── fileInventoryDifference.xml
        │         ├── manifestInventory.xml
        │         ├── signatureCatalog.xml
        │         ├── versionAdditions.xml
        │         └── versionInventory.xml
        └── v0003
              ├── data
              │   └── metadata
              │       ├── contentMetadata.xml
              │       ├── descMetadata.xml
              │       ├── embargoMetadata.xml
              │       ├── events.xml
              │       ├── identityMetadata.xml
              │       ├── provenanceMetadata.xml
              │       ├── rightsMetadata.xml
              │       ├── technicalMetadata.xml
              │       ├── versionMetadata.xml
              │       └── workflows.xml
              └── manifests
                  ├── fileInventoryDifference.xml
                  ├── manifestInventory.xml
                  ├── signatureCatalog.xml
                  ├── versionAdditions.xml
                  └── versionInventory.xml
```

An OCFL inventory that tracks the `data` directory would include a
manifest comprised as follows. Note the absence of the `manifests`
directory, as we are not encapsulating the Moab object in an OCFL
object, and the presence of `contentDirectory` to specify `data` as the
preserved content directory:

```
{
  "digestAlgorithm": "sha512",
  "head": "v3",
  "id": "druid:bj102hs9687",
  "contentDirectory": "data",
  "manifest": {
    "98114a...588": [ "v0001/data/content/eric-smith-dissertation-augmented.pdf" ],
    "7f3d87...15b": [ "v0001/data/content/eric-smith-dissertation.pdf" ],
    "6d19f0...064": [ "v0001/data/metadata/technicalMetadata.xml" ],
    "6e4be4...375": [ "v0001/data/metadata/provenanceMetadata.xml" ],
    "d8a319...d0f": [ "v0001/data/metadata/descMetadata.xml" ],
    "de823a...acc": [ "v0001/data/metadata/rightsMetadata.xml" ],
    "080617...40c": [ "v0001/data/metadata/identityMetadata.xml" ],
    "e15267...58d": [ "v0001/data/metadata/versionMetadata.xml" ],
    "0d9e0b...9a2": [ "v0001/data/metadata/contentMetadata.xml" ],
    "dd9289...31d": [ "v0001/data/metadata/relationshipMetadata.xml" ],
    "7519c5...63f": [ "v0002/data/metadata/provenanceMetadata.xml" ],
    "abda4c...622": [ "v0002/data/metadata/workflows.xml" ],
    "76549e...b2b": [ "v0002/data/metadata/rightsMetadata.xml" ],
    "bdc4d6...3b6": [ "v0002/data/metadata/events.xml" ],
    "7b331c...f9b": [ "v0002/data/metadata/identityMetadata.xml" ],
    "80ceac...b9c": [ "v0002/data/metadata/versionMetadata.xml" ],
    "4853a2...fbe": [ "v0002/data/metadata/contentMetadata.xml" ],
    "1d5090...f5f": [ "v0002/data/metadata/relationshipMetadata.xml" ],
    "f209bf...ceb": [ "v0002/data/metadata/embargoMetadata.xml" ],
    "dd9125...d4b": [ "v0003/data/metadata/technicalMetadata.xml" ],
    "d9e177...477": [ "v0003/data/metadata/provenanceMetadata.xml" ],
    "4f5908...4f5": [ "v0003/data/metadata/workflows.xml" ],
    "e64db0...500": [ "v0003/data/metadata/descMetadata.xml" ],
    "05fa51...818": [ "v0003/data/metadata/rightsMetadata.xml" ],
    "d70dd8...5ad": [ "v0003/data/metadata/events.xml" ],
    "509a2d...dc6": [ "v0003/data/metadata/identityMetadata.xml" ],
    "548066...893": [ "v0003/data/metadata/versionMetadata.xml" ],
    "93884e...aae": [ "v0003/data/metadata/contentMetadata.xml" ],
    "4c5ab4...b02": [ "v0003/data/metadata/embargoMetadata.xml" ]
  },
  "type": "https://ocfl.io/1.1/spec/#inventory",
  "versions": {
    "v1": {
      "created": "2019-03-14T20:31:00Z",
      "state": {
        "98114a...588": [ "content/eric-smith-dissertation-augmented.pdf" ],
        "7f3d87...15b": [ "content/eric-smith-dissertation.pdf" ],
        "6d19f0...064": [ "metadata/technicalMetadata.xml" ],
        "6e4be4...375": [ "metadata/provenanceMetadata.xml" ],
        "d8a319...d0f": [ "metadata/descMetadata.xml" ],
        "de823a...acc": [ "metadata/rightsMetadata.xml" ],
        "080617...40c": [ "metadata/identityMetadata.xml" ],
        "e15267...58d": [ "metadata/versionMetadata.xml" ],
        "0d9e0b...9a2": [ "metadata/contentMetadata.xml" ],
        "dd9289...31d": [ "metadata/relationshipMetadata.xml" ]
      }
    },
    "v2": {
      "created": "2019-03-24T09:22:00Z",
      "state": {
        "98114a...588": [ "content/eric-smith-dissertation-augmented.pdf" ],
        "7f3d87...15b": [ "content/eric-smith-dissertation.pdf" ],
        "6d19f0...064": [ "metadata/technicalMetadata.xml" ],
        "7519c5...63f": [ "metadata/provenanceMetadata.xml" ],
        "d8a319...d0f": [ "metadata/descMetadata.xml" ],
        "76549e...b2b": [ "metadata/rightsMetadata.xml" ],
        "7b331c...f9b": [ "metadata/identityMetadata.xml" ],
        "80ceac...b9c": [ "metadata/versionMetadata.xml" ],
        "4853a2...fbe": [ "metadata/contentMetadata.xml" ],
        "1d5090...f5f": [ "metadata/relationshipMetadata.xml" ],
        "abda4c...622": [ "metadata/workflows.xml" ],
        "bdc4d6...3b6": [ "metadata/events.xml" ],
        "f209bf...ceb": [ "metadata/embargoMetadata.xml" ]
      }
    },
    "v3": {
      "created": "2019-04-02T11:07:00Z",
      "state": {
        "98114a...588": [ "content/eric-smith-dissertation-augmented.pdf" ],
        "7f3d87...15b": [ "content/eric-smith-dissertation.pdf" ],
        "dd9125...d4b": [ "metadata/technicalMetadata.xml" ],
        "d9e177...477": [ "metadata/provenanceMetadata.xml" ],
        "e64db0...500": [ "metadata/descMetadata.xml" ],
        "05fa51...818": [ "metadata/rightsMetadata.xml" ],
        "509a2d...dc6": [ "metadata/identityMetadata.xml" ],
        "548066...893": [ "metadata/versionMetadata.xml" ],
        "93884e...aae": [ "metadata/contentMetadata.xml" ],
        "1d5090...f5f": [ "metadata/relationshipMetadata.xml" ],
        "4f5908...4f5": [ "metadata/workflows.xml" ],
        "d70dd8...5ad": [ "metadata/events.xml" ],
        "4c5ab4...b02": [ "metadata/embargoMetadata.xml" ]
      }
    }
  }
}
```

### Example Extended OCFL Storage Root
{. #example-extended-storage-root}

The following example OCFL Storage Root has an extension containing
custom content. The OCFL Storage Root itself remains valid.

```
[storage root]
    ├── 0=ocfl_1.1
    ├── extensions
    │   └── 0000-example-extension
    │       └── file-example.txt
    ├── ocfl_1.1.txt
    └── ocfl_layout.json
```

### Example Extended OCFL Object
{. #example-extended-object}

The following example OCFL Object has an extension containing custom
content. The OCFL Object itself remains valid.

```
[object root]
    ├── 0=ocfl_object_1.1
    ├── inventory.json
    ├── inventory.json.sha512
    ├── extensions
    │   └── 0000-example-extension
    │       └── file1-draft.txt
    └── v1
        ├── inventory.json
        ├── inventory.json.sha512
        └── content
            └── file.txt
```
