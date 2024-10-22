# THIS FILE IS GENERATED FROM PADDLEPADDLE SETUP.PY
#
full_version     = '2.6.2'
major            = '2'
minor            = '6'
patch            = '2'
rc               = '0'
cuda_version     = 'False'
cudnn_version    = 'False'
xpu_version      = 'False'
xpu_xccl_version = 'False'
istaged          = True
commit           = '8ce0de584c570589117e403322f3d1a0de6554e5'
with_mkl         = 'ON'
cinn_version      = 'False'

__all__ = ['cuda', 'cudnn', 'show', 'xpu', 'xpu_xccl']

def show():
    """Get the version of paddle if `paddle` package if tagged. Otherwise, output the corresponding commit id.

    Returns:
        If paddle package is not tagged, the commit-id of paddle will be output.
        Otherwise, the following information will be output.

        full_version: version of paddle

        major: the major version of paddle

        minor: the minor version of paddle

        patch: the patch level version of paddle

        rc: whether it's rc version

        cuda: the cuda version of package. It will return `False` if CPU version paddle package is installed

        cudnn: the cudnn version of package. It will return `False` if CPU version paddle package is installed

        xpu: the xpu version of package. It will return `False` if non-XPU version paddle package is installed

        xpu_xccl: the xpu xccl version of package. It will return `False` if non-XPU version paddle package is installed

        cinn: the cinn version of package. It will return `False` if paddle package is not compiled with CINN

    Examples:
        .. code-block:: python

            >>> import paddle

            >>> # Case 1: paddle is tagged with 2.2.0
            >>> paddle.version.show()
            >>> # doctest: +SKIP('Different environments yield different output.')
            full_version: 2.2.0
            major: 2
            minor: 2
            patch: 0
            rc: 0
            cuda: '10.2'
            cudnn: '7.6.5'
            xpu: '20230114'
            xpu_xccl: '1.0.7'
            cinn: False
            >>> # doctest: -SKIP

            >>> # Case 2: paddle is not tagged
            >>> paddle.version.show()
            >>> # doctest: +SKIP('Different environments yield different output.')
            commit: cfa357e984bfd2ffa16820e354020529df434f7d
            cuda: '10.2'
            cudnn: '7.6.5'
            xpu: '20230114'
            xpu_xccl: '1.0.7'
            cinn: False
            >>> # doctest: -SKIP

    """
    if istaged:
        print('full_version:', full_version)
        print('major:', major)
        print('minor:', minor)
        print('patch:', patch)
        print('rc:', rc)
    else:
        print('commit:', commit)
    print('cuda:', cuda_version)
    print('cudnn:', cudnn_version)
    print('xpu:', xpu_version)
    print('xpu_xccl:', xpu_xccl_version)
    print('cinn:', cinn_version)

def mkl():
    return with_mkl

def cuda():
    """Get cuda version of paddle package.

    Returns:
        string: Return the version information of cuda. If paddle package is CPU version, it will return False.

    Examples:
        .. code-block:: python

            >>> import paddle

            >>> paddle.version.cuda()
            >>> # doctest: +SKIP('Different environments yield different output.')
            '10.2'

    """
    return cuda_version

def cudnn():
    """Get cudnn version of paddle package.

    Returns:
        string: Return the version information of cudnn. If paddle package is CPU version, it will return False.

    Examples:
        .. code-block:: python

            >>> import paddle

            >>> paddle.version.cudnn()
            >>> # doctest: +SKIP('Different environments yield different output.')
            '7.6.5'

    """
    return cudnn_version

def xpu():
    """Get xpu version of paddle package.

    Returns:
        string: Return the version information of xpu. If paddle package is non-XPU version, it will return False.

    Examples:
        .. code-block:: python

            >>> import paddle

            >>> paddle.version.xpu()
            >>> # doctest: +SKIP('Different environments yield different output.')
            '20230114'

    """
    return xpu_version

def xpu_xccl():
    """Get xpu xccl version of paddle package.

    Returns:
        string: Return the version information of xpu xccl. If paddle package is non-XPU version, it will return False.

    Examples:
        .. code-block:: python

            >>> import paddle

            >>> paddle.version.xpu_xccl()
            >>> # doctest: +SKIP('Different environments yield different output.')
            '1.0.7'

    """
    return xpu_xccl_version

def cinn():
    """Get CINN version of paddle package.

    Returns:
        string: Return the version information of CINN. If paddle package is not compiled with CINN, it will return False.

    Examples:
        .. code-block:: python

            >>> import paddle

            >>> paddle.version.cinn()
            >>> # doctest: +SKIP('Different environments yield different output.')
            False

    """
    return cinn_version
