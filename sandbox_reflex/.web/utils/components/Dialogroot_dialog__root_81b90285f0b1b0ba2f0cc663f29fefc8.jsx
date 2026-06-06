
import {Fragment,memo,useContext,useEffect} from "react"
import {isTrue} from "$/utils/state"
import {Dialog as RadixThemesDialog} from "@radix-ui/themes"
import {StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Dialogroot_dialog__root_81b90285f0b1b0ba2f0cc663f29fefc8 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state____auth_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state)



    return(
        jsx(RadixThemesDialog.Root,{open:reflex___state____state__sandbox_reflex___state____auth_state.is_profile_modal_open_rx_state_},children)
    )
});
