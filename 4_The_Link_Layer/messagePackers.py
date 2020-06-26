%load_ext autoreload
%autoreload 2

def packSwapResult(success, fidelity):
    return "swap-" + success + "-fidelity" + "-" + str(fidelity)

def packLinkCreationSuccess(success, fidelity):
    return "link-" + success + "-fidelity" + "-" + str(fidelity)

def packLinkRequest(repeaterId):
    return repeaterId + "-link-request"

def packLinkRequestDeny(repeaterId):
    return repeaterId + "-link-deny"

def packLinkRequestAccept(repeaterId):
    return repeaterId + "-link-accept"

def packLinkExpired(id):
    return id + "-link-expired"

def packQubitDecohered(qubitId):
    return qubitId + "-decohered"
